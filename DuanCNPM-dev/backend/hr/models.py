from django.db import models


class NhanVien(models.Model):
    manhanvien = models.AutoField(primary_key=True)
    hoten = models.CharField(max_length=100)
    vaitro = models.CharField(max_length=50, null=True, blank=True)
    sdt = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    diachi = models.CharField(max_length=200, null=True, blank=True)
    luong = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ngayvaolam = models.DateField(null=True, blank=True)
    calam = models.CharField(max_length=50, null=True, blank=True)
    ghichu = models.CharField(max_length=500, null=True, blank=True)
    trangthai = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'NHANVIEN'
        managed = False

    def __str__(self):
        return self.hoten


class HopDong(models.Model):
    mahopdonglaodong = models.AutoField(primary_key=True)
    manhanvien = models.IntegerField()
    loaihopdong = models.CharField(max_length=50)
    ngaybatdau = models.DateField()
    ngayketthuc = models.DateField(null=True, blank=True)
    luongcoban = models.DecimalField(max_digits=18, decimal_places=2)
    phucap = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ghichu = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'HOPDONG'
        managed = False


class ChamCong(models.Model):
    machamcong = models.AutoField(primary_key=True)
    manhanvien = models.IntegerField()
    ngaylam = models.DateField()
    giovao = models.TimeField()
    giora = models.TimeField(null=True, blank=True)
    ghichu = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'CHAMCONG'
        managed = False
