# quanly/models.py
from django.db import models


# TRẠNG THÁI
TRANG_THAI_PHONG = [
    ('TRONG', 'Trống'),
    ('DANG_THUE', 'Đang thuê'),
    ('BAO_TRI', 'Đang bảo trì'),
]

TRANG_THAI_DATPHONG = [
    ('CHO', 'Chờ'),
    ('XAC_NHAN', 'Xác nhận'),
    ('DANG_O', 'Đang ở'),
    ('HOAN_TAT', 'Hoàn tất'),
    ('HUY', 'Hủy'),
]

TRANG_THAI_HOADON = [
    ('CHUA', 'Chưa thanh toán'),
    ('DA', 'Đã thanh toán'),
    ('HUY', 'Hủy'),
]


class LoaiPhong(models.Model):
    maloai = models.AutoField(db_column='MaLoai', primary_key=True)
    ten = models.CharField(max_length=100, db_column='TenLoai')
    mota = models.TextField(blank=True, null=True, db_column='MoTa')
    giacoban = models.DecimalField(max_digits=18, decimal_places=0, db_column='GiaCoBan')

    class Meta:
        db_table = 'LoaiPhong'
        managed = False
        verbose_name = 'Loại phòng'
        verbose_name_plural = 'Loại phòng'

    def __str__(self):
        return self.ten


class Phong(models.Model):
    maphong = models.AutoField(db_column='MaPhong', primary_key=True)
    sophong = models.CharField(max_length=10, unique=True, db_column='SoPhong')
    loai = models.ForeignKey(LoaiPhong, on_delete=models.PROTECT, db_column='MaLoai', related_name='phongs')
    trangthai = models.CharField(max_length=20, choices=TRANG_THAI_PHONG, default='TRONG', db_column='TrangThai')
    ngungkdd = models.BooleanField(default=False, db_column='NgungKinhDoanh')

    class Meta:
        db_table = 'Phong'
        managed = False
        ordering = ['sophong']
        verbose_name = 'Phòng'
        verbose_name_plural = 'Phòng'

    def __str__(self):
        return self.sophong


class KhachHang(models.Model):
    makh = models.AutoField(db_column='MaKH', primary_key=True)
    hoten = models.CharField(max_length=150, db_column='HoTen')
    cccd = models.CharField(max_length=20, blank=True, null=True, unique=True, db_column='CCCD')
    sodt = models.CharField(max_length=20, blank=True, null=True, db_column='SoDT')
    email = models.EmailField(blank=True, null=True, db_column='Email')
    diachi = models.CharField(max_length=255, blank=True, null=True, db_column='DiaChi')
    ngunghd = models.BooleanField(default=False, db_column='NgungHoatDong')

    class Meta:
        db_table = 'KhachHang'
        managed = False
        verbose_name = 'Khách hàng'
        verbose_name_plural = 'Khách hàng'

    def __str__(self):
        return self.hoten


class NhanVien(models.Model):
    manv = models.AutoField(db_column='MaNV', primary_key=True)
    hoten = models.CharField(max_length=150, db_column='HoTen')
    chucvu = models.CharField(max_length=50, db_column='ChucVu')
    sodt = models.CharField(max_length=20, blank=True, null=True, db_column='SoDT')
    email = models.EmailField(blank=True, null=True, db_column='Email')
    taikhoan = models.CharField(max_length=50, unique=True, db_column='TaiKhoan')
    matkhau = models.CharField(max_length=255, db_column='MatKhau')
    ngunghd = models.BooleanField(default=False, db_column='NgungHoatDong')

    class Meta:
        db_table = 'NhanVien'
        managed = False
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

    def __str__(self):
        return f"{self.hoten} ({self.chucvu})"


class CongTacVien(models.Model):
    mactv = models.AutoField(db_column='MaCTV', primary_key=True)
    hoten = models.CharField(max_length=150, db_column='HoTen')
    sdt = models.CharField(max_length=20, blank=True, null=True, db_column='SDT')
    zalo = models.CharField(max_length=20, blank=True, null=True, db_column='Zalo')
    ghichu = models.TextField(blank=True, null=True, db_column='GhiChu')
    ngunghop = models.BooleanField(default=False, db_column='NgungHopTac')

    class Meta:
        db_table = 'CongTacVien'
        managed = False
        verbose_name = 'Cộng tác viên'
        verbose_name_plural = 'Cộng tác viên'

    def __str__(self):
        return self.hoten


class DatPhong(models.Model):
    madp = models.AutoField(db_column='MaDP', primary_key=True)
    khach = models.ForeignKey(KhachHang, on_delete=models.PROTECT, db_column='MaKH', related_name='datphongs')
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.PROTECT, db_column='MaNV', related_name='datphongs')
    loaikhach = models.CharField(max_length=50, db_column='LoaiKhach')
    ngaynhan = models.DateField(db_column='NgayNhan')
    ngaytra = models.DateField(db_column='NgayTra')
    trangthai = models.CharField(max_length=20, choices=TRANG_THAI_DATPHONG, default='CHO', db_column='TrangThai')
    ctv = models.ForeignKey(CongTacVien, null=True, blank=True, on_delete=models.SET_NULL, db_column='MaCTV')
    ghichu = models.TextField(blank=True, null=True, db_column='GhiChu')
    created_at = models.DateTimeField(auto_now_add=True, db_column='Created_at')

    class Meta:
        db_table = 'DatPhong'
        managed = False
        verbose_name = 'Đặt phòng'
        verbose_name_plural = 'Đặt phòng'

    def __str__(self):
        return f"DP#{self.madp} - {self.khach}"


class CT_DatPhong(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    datphong = models.ForeignKey(DatPhong, on_delete=models.CASCADE, related_name='chitiet', db_column='MaDP')
    phong = models.ForeignKey(Phong, on_delete=models.PROTECT, db_column='MaPhong')
    giaphong = models.DecimalField(max_digits=18, decimal_places=0, db_column='GiaPhong')

    class Meta:
        db_table = 'CT_DatPhong'
        managed = False
        verbose_name = 'Chi tiết đặt phòng'
        verbose_name_plural = 'Chi tiết đặt phòng'

    def __str__(self):
        return f"{self.datphong} - {self.phong}"


class DichVu(models.Model):
    madv = models.AutoField(db_column='MaDV', primary_key=True)
    ten = models.CharField(max_length=150, db_column='TenDV')
    dongia = models.DecimalField(max_digits=18, decimal_places=0, db_column='DonGia')
    donvi = models.CharField(max_length=50, db_column='DonVi')
    ngung = models.BooleanField(default=False, db_column='NgungCungCap')

    class Meta:
        db_table = 'DichVu'
        managed = False
        verbose_name = 'Dịch vụ'
        verbose_name_plural = 'Dịch vụ'

    def __str__(self):
        return self.ten


class HoaDon(models.Model):
    mahd = models.AutoField(db_column='MaHD', primary_key=True)
    datphong = models.ForeignKey(DatPhong, null=True, blank=True, on_delete=models.SET_NULL, db_column='MaDP', related_name='hoadons')
    khach = models.ForeignKey(KhachHang, on_delete=models.PROTECT, db_column='MaKH', related_name='hoadons')
    ngaylap = models.DateTimeField(auto_now_add=True, db_column='NgayLap')
    tongtien = models.DecimalField(max_digits=14, decimal_places=0, default=0, db_column='TongTien')
    trangthai = models.CharField(max_length=10, choices=TRANG_THAI_HOADON, default='CHUA', db_column='TrangThai')

    class Meta:
        db_table = 'HoaDon'
        managed = False
        verbose_name = 'Hóa đơn'
        verbose_name_plural = 'Hóa đơn'

    def __str__(self):
        return f"HD#{self.mahd} - {self.khach}"


class CT_HoaDon(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    hoadon = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name='chitiet', db_column='MaHD')
    loai = models.CharField(max_length=50, db_column='Loai')
    mathamchieu = models.IntegerField(null=True, blank=True, db_column='MaThamChieu')
    mota = models.CharField(max_length=255, blank=True, null=True, db_column='MoTa')
    soluong = models.IntegerField(default=1, db_column='SoLuong')
    dongia = models.DecimalField(max_digits=18, decimal_places=0, db_column='DonGia')

    class Meta:
        db_table = 'CT_HoaDon'
        managed = False
        verbose_name = 'Chi tiết hóa đơn'
        verbose_name_plural = 'Chi tiết hóa đơn'

    def __str__(self):
        return f"{self.hoadon} - {self.loai} ({self.soluong} x {self.dongia})"

    @property
    def thanhtien(self):
        return (self.soluong or 0) * (self.dongia or 0)


class DoiNha(models.Model):
    matask = models.AutoField(db_column='MaTask', primary_key=True)
    phong = models.ForeignKey(Phong, on_delete=models.CASCADE, db_column='MaPhong')
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='MaNV')
    ngaytao = models.DateTimeField(auto_now_add=True, db_column='NgayTao')
    trangthai = models.CharField(max_length=20, choices=[('CANDON','Cần dọn'),('DANGDON','Đang dọn'),('DADON','Đã dọn')], default='CANDON', db_column='TrangThai')
    ghichu = models.TextField(blank=True, null=True, db_column='GhiChu')

    class Meta:
        db_table = 'DoiNha'
        managed = False
        verbose_name = 'Dội nhà'
        verbose_name_plural = 'Dội nhà'

    def __str__(self):
        return f"Task#{self.matask} - Phòng {self.phong}"


class ChamCong(models.Model):
    macong = models.AutoField(db_column='MaCong', primary_key=True)
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column='MaNV')
    ngay = models.DateField(db_column='Ngay')
    trangthai = models.CharField(max_length=20, db_column='TrangThai')
    sogio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='SoGio')

    class Meta:
        db_table = 'ChamCong'
        managed = False
        verbose_name = 'Chấm công'
        verbose_name_plural = 'Chấm công'

    def __str__(self):
        return f"{self.nhanvien} - {self.ngay}"


class AuditLog(models.Model):
    malog = models.AutoField(db_column='MaLog', primary_key=True)
    thoigian = models.DateTimeField(auto_now_add=True, db_column='ThoiGian')
    manv = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, db_column='MaNV')
    hanhdong = models.CharField(max_length=255, db_column='HanhDong')
    bang = models.CharField(max_length=100, db_column='Bang')
    khoachinh = models.CharField(max_length=100, db_column='KhoaChinh')
    noidung = models.TextField(db_column='NoiDung')

    class Meta:
        db_table = 'AuditLog'
        managed = False
        verbose_name = 'Nhật ký'
        verbose_name_plural = 'Nhật ký'

    def __str__(self):
        return f"{self.thoigian} - NV:{self.manv} - {self.hanhdong}"
