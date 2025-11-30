from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Phong, LoaiPhong, DichVu, DatPhong, CT_DatPhong, HoaDon, KhachHang
from .forms import DatPhongForm, CTDatPhongInlineForm, KhachHangForm, CongTacVienForm
from .services import check_booking_conflict, do_checkin, do_checkout
from django.db import transaction, connection
from django.http import HttpResponse
from django.urls import reverse

def index(request):
    return HttpResponse("Trang quản lý hoạt động!")


def trang_chu(request):
    stats = {
        'tong_phong': Phong.objects.count(),
        'phong_trong': Phong.objects.filter(trangthai='TRONG').count(),
        'phong_thue': Phong.objects.filter(trangthai='DANG_THUE').count(),
    }
    return render(request, 'trang_chu.html', {'stats': stats})

def danh_sach_phong(request):
    phongs = Phong.objects.select_related('loai').all().order_by('sophong')
    return render(request, 'danh_sach_phong.html', {'phongs': phongs})

def chi_tiet_phong(request, pk):
    """
    Hiện trang chi tiết phòng + xử lý cập nhật trạng thái (POST).
    pk: dùng p.pk (không phụ thuộc tên cột PK).
    """
    phong = get_object_or_404(Phong, pk=pk)

    # Lấy choices của field trangthai để render select
    trangthai_choices = Phong._meta.get_field('trangthai').choices

    if request.method == 'POST':
        new_tt = request.POST.get('trangthai')
        if new_tt and new_tt in dict(trangthai_choices):
            phong.trangthai = new_tt
            phong.save()  # vì models managed=False nhưng vẫn cho phép update
            messages.success(request, "Cập nhật trạng thái phòng thành công.")
        else:
            messages.error(request, "Giá trị trạng thái không hợp lệ.")
        return redirect(reverse('quanly:chi_tiet_phong', args=[phong.pk]))

    # GET: hiển thị chi tiết
    # Bạn có thể truyền thêm dữ liệu (ví dụ lịch đặt phòng, dọn phòng...) nếu muốn
    context = {
        'phong': phong,
        'trangthai_choices': trangthai_choices,
    }
    return render(request, 'chi_tiet_phong.html', context)


def them_congtacvien(request):
    """
    Trang thêm cộng tác viên (simple page). Sau khi lưu sẽ redirect về dat_phong để người dùng chọn.
    """
    if request.method == 'POST':
        form = CongTacVienForm(request.POST)
        if form.is_valid():
            ctv = form.save()
            messages.success(request, f"Đã thêm cộng tác viên: {ctv.hoten}")
            # quay về trang đặt phòng (nếu bạn muốn về trang danh sách CTV thì đổi url)
            return redirect('quanly:dat_phong')
    else:
        form = CongTacVienForm()
    return render(request, 'them_congtacvien.html', {'form': form})


def danh_sach_dich_vu(request):
    ds = DichVu.objects.filter(ngung=False)
    return render(request, 'danh_sach_dich_vu.html', {'dichvus': ds})

def dat_phong(request):
    """
    Tạo DatPhong (chọn khách có sẵn hoặc tạo KhachHang mới),
    sau đó redirect sang them_chi_tiet_datphong để thêm phòng cụ thể.
    """
    if request.method == 'POST':
        form = DatPhongForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    dp = form.save(commit=False)
                    dp.trangthai = 'CHO'  # mặc định chờ
                    dp.save()
                    messages.success(request, "Đặt phòng đã được tạo. Tiếp theo thêm phòng vào booking.")
                    return redirect('quanly:them_chi_tiet_datphong', datphong_id=dp.id)
            except Exception as e:
                messages.error(request, f"Tạo đặt phòng thất bại: {e}")
        else:
            messages.error(request, "Dữ liệu không hợp lệ, kiểm tra lại.")
    else:
        form = DatPhongForm()
    return render(request, 'dat_phong.html', {'form': form})

def them_chi_tiet_datphong(request, datphong_id):
    dp = get_object_or_404(DatPhong, pk=datphong_id)
    if request.method == 'POST':
        form = CTDatPhongInlineForm(request.POST)
        if form.is_valid():
            phong = form.cleaned_data['phong']
            ngaynhan = dp.ngaynhan
            ngaytra = dp.ngaytra
            # kiểm tra xung đột
            if check_booking_conflict(phong.id, ngaynhan, ngaytra):
                messages.error(request, f"Phòng {phong.sophong} đã có đặt trùng trong khoảng này.")
            else:
                try:
                    with transaction.atomic():
                        ct = form.save(commit=False)
                        ct.datphong = dp
                        ct.save()
                        # cập nhật trạng thái phòng tạm: 'DANG_THUE'
                        phong.trangthai = 'DANG_THUE'
                        phong.save()
                        messages.success(request, f"Đã thêm phòng {phong.sophong} vào booking.")
                        return redirect('quanly:chi_tiet_datphong', pk=dp.id)
                except Exception as e:
                    messages.error(request, f"Lưu chi tiết thất bại: {e}")
        else:
            messages.error(request, "Dữ liệu chi tiết không hợp lệ.")
    else:
        form = CTDatPhongInlineForm()
    return render(request, 'them_chi_tiet_datphong.html', {'form': form, 'dp': dp})

def them_khachhang(request):
    if request.method == 'POST':
        form = KhachHangForm(request.POST)
        if form.is_valid():
            kh = form.save()
            # redirect về trang đặt phòng (hoặc danh sách phòng)
            messages.success(request, "Đã thêm khách hàng.")
            # nếu bạn muốn quay lại form đặt phòng:
            return redirect('quanly:dat_phong')
    else:
        form = KhachHangForm()
    return render(request, 'them_khachhang.html', {'form': form})
def chi_tiet_datphong(request, pk):
    dp = get_object_or_404(DatPhong, pk=pk)
    return render(request, 'chi_tiet_datphong.html', {'dp': dp})

@login_required
def checkin_view(request, datphong_id):
    # chỉ nhân viên có quyền mới gọi được (kiểm ở decorator/permission)
    try:
        do_checkin(datphong_id, request.user.id)
        messages.success(request, "Check-in thành công.")
    except Exception as e:
        messages.error(request, f"Check-in lỗi: {e}")
    return redirect('quanly:chi_tiet_datphong', datphong_id)

@login_required
def checkout_view(request, datphong_id):
    try:
        hd = do_checkout(datphong_id, request.user.id)
        messages.success(request, f"Check-out hoàn tất. Hóa đơn #{hd.id} được tạo.")
        return redirect('quanly:tao_hoa_don', hd.id)
    except Exception as e:
        messages.error(request, f"Check-out lỗi: {e}")
        return redirect('quanly:chi_tiet_datphong', datphong_id)

# Gọi stored procedure ví dụ (nếu bạn muốn gọi sp trên SQL Server)
def call_proc_example(request):
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_them_dichvu @TenDV=%s, @DonGia=%s, @DonVi=%s", ['Test DV', 10000, '1 cái'])
        row = cursor.fetchone()  # nếu proc trả SCOPE_IDENTITY
    return HttpResponse(f"SP trả: {row}")

from django.utils import timezone

def tao_hoa_don(request, pk):
    """
    Tạo hóa đơn cho DatPhong có id = pk.
    Logic mẫu:
    - Lấy DatPhong
    - Tổng tiền = tổng (số lượng * đơn giá) từ CT_DatPhong hoặc tính theo phòng/dịch vụ
    - Tạo HoaDon liên kết tới DatPhong, lưu tổng tiền, trả về redirect/hoặc render
    NOTE: chỉnh trường/tên model nếu khác.
    """
    dp = get_object_or_404(DatPhong, pk=pk)

    # Tính tổng tiền: ví dụ tổng đơn giản từ CT_DatPhong nếu CT_DatPhong có trường 'thanh_tien'
    total = 0
    cts = CT_DatPhong.objects.filter(datphong=dp)
    for ct in cts:
        # Nếu bạn có trường 'thanh_tien' hoặc 'don_gia'/'so_luong' -> chỉnh ở đây
        if hasattr(ct, 'thanh_tien'):
            total += (ct.thanh_tien or 0)
        elif hasattr(ct, 'don_gia') and hasattr(ct, 'so_luong'):
            total += (ct.don_gia or 0) * (ct.so_luong or 1)
        else:
            # fallback: nếu không có gì, bạn có thể tính giá theo phòng->loai->gia
            try:
                total += (ct.phong.loai.gia or 0)
            except Exception:
                pass

    # Nếu bạn có thêm dịch vụ riêng (CT dịch vụ) hãy cộng vào total tương tự

    # Tạo hóa đơn an toàn trong transaction
    try:
        with transaction.atomic():
            hd = HoaDon.objects.create(
                datphong = dp,
                ngay = timezone.now(),
                tong_tien = total
            )
            # nếu cần tạo các dòng chi tiết hóa đơn, làm ở đây
            # ví dụ: tạo HD chi tiết từ CT_DatPhong (nếu có model HoaDonChiTiet)
            messages.success(request, f"Hóa đơn #{hd.id} đã được tạo (Tổng {total}).")
    except Exception as e:
        messages.error(request, f"Tạo hóa đơn thất bại: {e}")
        return redirect('quanly:chi_tiet_datphong', pk)

    # chuyển đến trang hiển thị hóa đơn (nếu có) hoặc trang chi tiết đặt phòng
    return redirect('quanly:chi_tiet_datphong', pk)
