from django.db import models


class ThongBao(models.Model):
    mathongbao = models.AutoField(primary_key=True)
    tieude = models.CharField(max_length=200)
    noidung = models.TextField()
    nguoigui = models.IntegerField()  # FK tới TAIKHOAN.mataikhoan
    ngaygui = models.DateTimeField()

    class Meta:
        db_table = 'THONGBAO'
        managed = False

    def __str__(self):
        return self.tieude


class ThongBaoNhanVien(models.Model):
    mathongbao = models.IntegerField()
    mataikhoan = models.IntegerField()
    ngaydoc = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'THONGBAO_NHANVIEN'
        managed = False
        unique_together = ('mathongbao', 'mataikhoan')
