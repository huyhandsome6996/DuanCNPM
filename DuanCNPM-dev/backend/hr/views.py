from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import TaiKhoan
from .models import NhanVien


@login_required
def profile(request):
    user: TaiKhoan = request.user
    nhanvien = None
    try:
        nhanvien = NhanVien.objects.get(manhanvien=user.manhanvien)
    except NhanVien.DoesNotExist:
        nhanvien = None

    return render(request, 'hr/profile.html', {'nhanvien': nhanvien})
