from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from accounts.models import TaiKhoan
from .models import KhachHang, Phong, DatPhong
from .forms import KhachHangForm, PhongForm, DatPhongForm


# =============== DASHBOARD ===============

@login_required
def dashboard(request):
    """
    Dashboard chung: chuyển hướng theo vai trò.
    """
    user: TaiKhoan = request.user

    if user.vaitro == "QUANLY":
        return redirect("hotel:dashboard_manager")
    elif user.vaitro == "NHANVIEN":
        return redirect("hotel:dashboard_employee")

    return HttpResponse("Không xác định vai trò của tài khoản!")


@login_required
def dashboard_manager(request):
    """Dashboard dành cho QUẢN LÝ – được phép quản lý toàn hệ thống."""
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Bạn không có quyền truy cập trang quản lý!")

    # Thống kê đơn giản (em có thể cải tiến thêm sau)
    total_rooms = Phong.objects.count()
    total_customers = KhachHang.objects.count()
    active_bookings = DatPhong.objects.filter(ngaynhan__isnull=False, ngaytra__isnull=True).count()

    return render(request, "hotel/dashboard_manager.html", {
        "user": user,
        "total_rooms": total_rooms,
        "total_customers": total_customers,
        "active_bookings": active_bookings,
    })


@login_required
def dashboard_employee(request):
    """Dashboard dành cho NHÂN VIÊN – chỉ xem."""
    user: TaiKhoan = request.user
    if user.vaitro != "NHANVIEN":
        return HttpResponse("Bạn không có quyền truy cập trang nhân viên!")

    # Tạm thời cho hiển thị đơn giản
    return render(request, "hotel/dashboard_employee.html", {
        "user": user,
    })


# =============== QUẢN LÝ KHÁCH HÀNG (manager-only) ===============

@login_required
def customer_list(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được xem danh sách khách hàng.")
    customers = KhachHang.objects.all().order_by('-makhachhang')
    return render(request, "hotel/customers_list.html", {"customers": customers})


@login_required
def customer_create(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được thêm khách hàng.")

    if request.method == "POST":
        form = KhachHangForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm khách hàng thành công.")
            return redirect("hotel:customer_list")
    else:
        form = KhachHangForm()

    return render(request, "hotel/customer_form.html", {"form": form, "title": "Thêm khách hàng"})


@login_required
def customer_update(request, makhachhang):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được sửa khách hàng.")

    customer = get_object_or_404(KhachHang, makhachhang=makhachhang)

    if request.method == "POST":
        form = KhachHangForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật khách hàng thành công.")
            return redirect("hotel:customer_list")
    else:
        form = KhachHangForm(instance=customer)

    return render(request, "hotel/customer_form.html", {"form": form, "title": "Cập nhật khách hàng"})


@login_required
def customer_delete(request, makhachhang):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được xóa khách hàng.")

    customer = get_object_or_404(KhachHang, makhachhang=makhachhang)

    if request.method == "POST":
        customer.delete()
        messages.success(request, "Đã xóa khách hàng.")
        return redirect("hotel:customer_list")

    return render(request, "hotel/customer_confirm_delete.html", {"customer": customer})


# =============== QUẢN LÝ PHÒNG (manager-only) ===============

@login_required
def room_list(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được xem danh sách phòng.")

    rooms = Phong.objects.all().order_by('maphong')
    return render(request, "hotel/rooms_list.html", {"rooms": rooms})


@login_required
def room_create(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được thêm phòng.")

    if request.method == "POST":
        form = PhongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm phòng thành công.")
            return redirect("hotel:room_list")
    else:
        form = PhongForm()

    return render(request, "hotel/room_form.html", {"form": form, "title": "Thêm phòng"})


@login_required
def room_update(request, maphong):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được sửa phòng.")

    room = get_object_or_404(Phong, maphong=maphong)

    if request.method == "POST":
        form = PhongForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật phòng thành công.")
            return redirect("hotel:room_list")
    else:
        form = PhongForm(instance=room)

    return render(request, "hotel/room_form.html", {"form": form, "title": "Cập nhật phòng"})


@login_required
def room_delete(request, maphong):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được xóa phòng.")

    room = get_object_or_404(Phong, maphong=maphong)

    if request.method == "POST":
        room.delete()
        messages.success(request, "Đã xóa phòng.")
        return redirect("hotel:room_list")

    return render(request, "hotel/room_confirm_delete.html", {"room": room})


# =============== TẠO LƯỢT ĐẶT PHÒNG (manager-only) ===============

@login_required
def booking_create(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được tạo đặt phòng.")

    if request.method == "POST":
        form = DatPhongForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Nếu chưa nhập, tự set ngày đặt = thời điểm hiện tại
            if not booking.ngaydat:
                booking.ngaydat = timezone.now()

            booking.save()
            messages.success(request, "Tạo đặt phòng thành công.")
            return redirect("hotel:dashboard_manager")
        else:
            # Báo cho người dùng biết là dữ liệu sai
            messages.error(request, "Dữ liệu không hợp lệ, vui lòng kiểm tra các ô màu đỏ.")
    else:
        form = DatPhongForm()

    return render(request, "hotel/booking_form.html", {"form": form})

@login_required
def booking_list(request):
    """
    Danh sách các lượt đặt phòng.

    - Nếu là QUANLY: xem tất cả.
    - Nếu là NHANVIEN: chỉ xem các đặt phòng do mình (manhanvien) phụ trách.
    """
    user: TaiKhoan = request.user

    if user.vaitro == "QUANLY":
        bookings = DatPhong.objects.all().order_by('-madatphong')
    elif user.vaitro == "NHANVIEN":
        bookings = DatPhong.objects.filter(manhanvien=user.manhanvien).order_by('-madatphong')
    else:
        return HttpResponse("Tài khoản không có quyền xem danh sách đặt phòng.")

    return render(request, "hotel/bookings_list.html", {
        "bookings": bookings,
    })