from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Phong, LoaiPhong, DichVu, DatPhong, CT_DatPhong, HoaDon
from .forms import DatPhongForm, CTDatPhongInlineForm, KhachHangForm, ChonDichVuForm
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

def danh_sach_dich_vu(request):
    ds = DichVu.objects.filter(ngung=False)
    return render(request, 'danh_sach_dich_vu.html', {'dichvus': ds})

def dat_phong(request):
    """
    Giao diện đặt phòng: tạo KhachHang (nếu cần), tạo DatPhong, sau đó thêm CT_DatPhong (chọn phòng)
    Kiểm tra xung đột bằng check_booking_conflict
    """
    if request.method == 'POST':
        form = DatPhongForm(request.POST)
        if form.is_valid():
            dp = form.save(commit=False)
            # chưa commit chi tiết phòng ở đây
            dp.save()
            messages.success(request, "Đặt phòng đã tạo, tiếp theo chọn phòng vào booking.")
            return redirect('quanly:them_chi_tiet_datphong', dp.id)
    else:
        form = DatPhongForm()
    return render(request, 'dat_phong.html', {'form': form})

def them_chi_tiet_datphong(request, datphong_id):
    dp = get_object_or_404(DatPhong, pk=datphong_id)
    if request.method == 'POST':
        form = CTDatPhongInlineForm(request.POST, initial={'ngaynhan': dp.ngaynhan, 'ngaytra': dp.ngaytra})
        if form.is_valid():
            phong = form.cleaned_data['phong']
            # check conflict
            if check_booking_conflict(phong.id, dp.ngaynhan, dp.ngaytra):
                messages.error(request, f"Phòng {phong.sophong} đã có đặt trùng.")
            else:
                ct = form.save(commit=False)
                ct.datphong = dp
                ct.save()
                messages.success(request, "Thêm phòng vào booking thành công.")
                return redirect('quanly:chi_tiet_datphong', dp.id)
    else:
        form = CTDatPhongInlineForm()
    return render(request, 'them_chi_tiet_datphong.html', {'form': form, 'dp': dp})

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
