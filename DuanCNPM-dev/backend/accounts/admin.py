from django.contrib import admin
from .models import TaiKhoan

@admin.register(TaiKhoan)
class TaiKhoanAdmin(admin.ModelAdmin):
    list_display = ('mataikhoan', 'tendangnhap', 'vaitro', 'is_active')
