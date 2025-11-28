from django.contrib import admin
from .models import *

@admin.register(LoaiPhong)
class LoaiPhongAdmin(admin.ModelAdmin):
    list_display = ('ten','giacoban')

@admin.register(Phong)
class PhongAdmin(admin.ModelAdmin):
    list_display = ('sophong','loai','trangthai','ngungkdd')
    list_filter = ('trangthai','loai')

@admin.register(KhachHang)
class KhachHangAdmin(admin.ModelAdmin):
    list_display = ('hoten','cccd','sodt','ngunghd')

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('hoten','chucvu','taikhoan','ngunghd')
    search_fields = ('hoten','taikhoan')

# đăng ký các model khác
admin.site.register(CongTacVien)
admin.site.register(DatPhong)
admin.site.register(CT_DatPhong)
admin.site.register(DichVu)
admin.site.register(HoaDon)
admin.site.register(CT_HoaDon)
admin.site.register(DoiNha)
admin.site.register(ChamCong)
admin.site.register(AuditLog)
