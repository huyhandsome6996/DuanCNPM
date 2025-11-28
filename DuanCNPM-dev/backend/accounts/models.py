from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class TaiKhoanManager(BaseUserManager):
    def create_user(self, tendangnhap, password=None, **extra_fields):
        if not tendangnhap:
            raise ValueError("Tài khoản phải có tên đăng nhập")
        user = self.model(tendangnhap=tendangnhap, **extra_fields)
        if password:
            user.set_password(password)
        else:
            # nếu không truyền password, đặt tạm
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, tendangnhap, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('vaitro', 'QUANLY')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser phải có is_superuser=True')
        return self.create_user(tendangnhap, password, **extra_fields)


class TaiKhoan(AbstractBaseUser, PermissionsMixin):
    """
    Map với bảng TAIKHOAN trong SQL Server.
    """
    mataikhoan = models.AutoField(primary_key=True)
    tendangnhap = models.CharField(max_length=50, unique=True)

    # Các field này Django thêm sẵn trong AbstractBaseUser & PermissionsMixin:
    # password, last_login, is_superuser, groups, user_permissions

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    manhanvien = models.IntegerField()
    vaitro = models.CharField(max_length=20)  # 'QUANLY' hoặc 'NHANVIEN'

    objects = TaiKhoanManager()

    USERNAME_FIELD = 'tendangnhap'
    REQUIRED_FIELDS = []  # có thể thêm 'manhanvien' nếu muốn

    class Meta:
        db_table = 'TAIKHOAN'
        managed = False  # không cho Django tự tạo / sửa bảng

    def __str__(self):
        return self.tendangnhap
