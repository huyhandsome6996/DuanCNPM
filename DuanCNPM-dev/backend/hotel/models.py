from django.db import models


class KhachHang(models.Model):
    makhachhang = models.AutoField(primary_key=True)
    hoten = models.CharField(max_length=100)
    cccd = models.CharField(max_length=12, unique=True, null=True, blank=True)
    sdt = models.CharField(max_length=15, null=True, blank=True)
    loaikhach = models.CharField(max_length=50, null=True, blank=True)
    quoctich = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'KHACHHANG'
        managed = False

    def __str__(self):
        return self.hoten


class Phong(models.Model):
    maphong = models.CharField(max_length=3, primary_key=True)
    loaiphong = models.CharField(max_length=50)
    giaphong = models.DecimalField(max_digits=18, decimal_places=2)
    trangthai = models.CharField(max_length=30)

    class Meta:
        db_table = 'PHONG'
        managed = False

    def __str__(self):
        return f"Phòng {self.maphong} - {self.loaiphong}"



class KhuyenMai(models.Model):
    makhuyenmai = models.AutoField(primary_key=True)
    tenchuongtrinh = models.CharField(max_length=200)
    ngaybatdau = models.DateField()
    ngayketthuc = models.DateField()
    mucthamgia = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'KHUYENMAI'
        managed = False

    def __str__(self):
        return self.tenchuongtrinh


class DatPhong(models.Model):
    madatphong = models.AutoField(primary_key=True)
    makhachhang = models.IntegerField()
    maphong = models.IntegerField()
    manhanvien = models.IntegerField()
    ngaydat = models.DateTimeField()
    ngaynhan = models.DateTimeField(null=True, blank=True)
    ngaytra = models.DateTimeField(null=True, blank=True)
    tiendatcoc = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    mahoadon = models.IntegerField(null=True, blank=True)
    ngaylaphoadon = models.DateTimeField(null=True, blank=True)
    tongtien = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ghichu = models.CharField(max_length=500, null=True, blank=True)
    makhuyenmai = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'DATPHONG'
        managed = False

    def __str__(self):
        return f"Đặt phòng #{self.madatphong}"


class DichVu(models.Model):
    madichvu = models.AutoField(primary_key=True)
    tendichvu = models.CharField(max_length=100)
    loaidichvu = models.CharField(max_length=50, null=True, blank=True)
    dongia = models.DecimalField(max_digits=18, decimal_places=2)
    donvi = models.CharField(max_length=20, null=True, blank=True)
    mota = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'DICHVU'
        managed = False

    def __str__(self):
        return self.tendichvu


class ChiTietHoaDon(models.Model):
    mahoadon = models.IntegerField()
    madichvu = models.IntegerField()
    soluong = models.IntegerField()
    dongia = models.DecimalField(max_digits=18, decimal_places=2)
    thanhtien = models.DecimalField(max_digits=18, decimal_places=2)
    ghichu = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'CHITIETHOADON'
        managed = False
        unique_together = ('mahoadon', 'madichvu')
