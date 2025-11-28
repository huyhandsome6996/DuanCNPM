from django.db import models
from django.utils import timezone

# Trạng thái dùng cho hiển thị / DB
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
    ten = models.CharField(max_length=100)
    mota = models.TextField(blank=True, null=True)
    giacoban = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return self.ten

class Phong(models.Model):
    sophong = models.CharField(max_length=10, unique=True)
    loai = models.ForeignKey(LoaiPhong, on_delete=models.PROTECT)
    trangthai = models.CharField(max_length=20, choices=TRANG_THAI_PHONG, default='TRONG')
    ngungkdd = models.BooleanField(default=False)  # ngừng kinh doanh

    def __str__(self):
        return self.sophong

class KhachHang(models.Model):
    hoten = models.CharField(max_length=150)
    cccd = models.CharField(max_length=20, blank=True, null=True, unique=True)
    sodt = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    diachi = models.CharField(max_length=255, blank=True, null=True)
    ngunghd = models.BooleanField(default=False)

    def __str__(self):
        return self.hoten

class NhanVien(models.Model):
    hoten = models.CharField(max_length=150)
    chucvu = models.CharField(max_length=50)
    sodt = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    taikhoan = models.CharField(max_length=50, unique=True)
    matkhau = models.CharField(max_length=255)  # Lưu hash nếu dùng thực tế
    ngunghd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hoten} ({self.chucvu})"

class CongTacVien(models.Model):
    hoten = models.CharField(max_length=150)
    sdt = models.CharField(max_length=20, blank=True, null=True)
    zalo = models.CharField(max_length=20, blank=True, null=True)
    ghichu = models.TextField(blank=True, null=True)
    ngunghop = models.BooleanField(default=False)

    def __str__(self):
        return self.hoten

class DatPhong(models.Model):
    khach = models.ForeignKey(KhachHang, on_delete=models.PROTECT)
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.PROTECT)
    loaikhach = models.CharField(max_length=50)  # Vãng lai, Tour, Booking, Agoda, Traveloka
    ngaynhan = models.DateField()
    ngaytra = models.DateField()
    trangthai = models.CharField(max_length=20, choices=TRANG_THAI_DATPHONG, default='CHO')
    ctv = models.ForeignKey(CongTacVien, null=True, blank=True, on_delete=models.SET_NULL)
    ghichu = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DP#{self.id} - {self.khach}"

class CT_DatPhong(models.Model):
    datphong = models.ForeignKey(DatPhong, on_delete=models.CASCADE, related_name='chitiet')
    phong = models.ForeignKey(Phong, on_delete=models.PROTECT)
    giaphong = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f"{self.datphong} - {self.phong}"

class DichVu(models.Model):
    ten = models.CharField(max_length=150)
    dongia = models.DecimalField(max_digits=12, decimal_places=0)
    donvi = models.CharField(max_length=50)
    ngung = models.BooleanField(default=False)

    def __str__(self):
        return self.ten

class HoaDon(models.Model):
    datphong = models.ForeignKey(DatPhong, null=True, blank=True, on_delete=models.SET_NULL)
    khach = models.ForeignKey(KhachHang, on_delete=models.PROTECT)
    ngaylap = models.DateTimeField(auto_now_add=True)
    tongtien = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    trangthai = models.CharField(max_length=10, choices=TRANG_THAI_HOADON, default='CHUA')

    def __str__(self):
        return f"HD#{self.id} - {self.khach}"

class CT_HoaDon(models.Model):
    hoadon = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name='chitiet')
    loai = models.CharField(max_length=50)  # 'PHONG' / 'DICHVU' / 'PHUTHU'
    mathamchieu = models.IntegerField(null=True, blank=True)
    mota = models.CharField(max_length=255, blank=True, null=True)
    soluong = models.IntegerField(default=1)
    dongia = models.DecimalField(max_digits=12, decimal_places=0)

    @property
    def thanhtien(self):
        return self.soluong * self.dongia

class DoiNha(models.Model):
    phong = models.ForeignKey(Phong, on_delete=models.CASCADE)
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ngaytao = models.DateTimeField(auto_now_add=True)
    trangthai = models.CharField(max_length=20, choices=[('CANDON','Cần dọn'),('DANGDON','Đang dọn'),('DADON','Đã dọn')], default='CANDON')
    ghichu = models.TextField(blank=True, null=True)

class ChamCong(models.Model):
    nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ngay = models.DateField()
    trangthai = models.CharField(max_length=20)
    sogio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class AuditLog(models.Model):
    thoigian = models.DateTimeField(auto_now_add=True)
    manv = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True)
    hanhdong = models.CharField(max_length=255)
    bang = models.CharField(max_length=100)
    khoachinh = models.CharField(max_length=100)
    noidung = models.TextField()
