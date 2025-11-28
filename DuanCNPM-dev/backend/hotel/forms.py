from django import forms
from .models import KhachHang, Phong, DatPhong


class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['hoten', 'cccd', 'sdt', 'loaikhach', 'quoctich']
        widgets = {
            'hoten': forms.TextInput(attrs={'class': 'form-control'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control'}),
            'loaikhach': forms.TextInput(attrs={'class': 'form-control'}),
            'quoctich': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PhongForm(forms.ModelForm):
    class Meta:
        model = Phong
        fields = ['maphong', 'loaiphong', 'giaphong', 'trangthai']
        widgets = {
            'maphong': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 201'}),
            'loaiphong': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thường / VIP...'}),
            'giaphong': forms.NumberInput(attrs={'class': 'form-control'}),
            'trangthai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trống / Đang ở / Bảo trì'}),
        }



class DatPhongForm(forms.ModelForm):
    class Meta:
        model = DatPhong
        fields = [
            'makhachhang', 'maphong', 'manhanvien',
            'ngaydat', 'ngaynhan', 'ngaytra',
            'tiendatcoc', 'ghichu', 'makhuyenmai'
        ]
        widgets = {
            'makhachhang': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mã khách'}),
            'maphong': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: 201'}),
            'manhanvien': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mã nhân viên'}),
            'ngaydat': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ngaynhan': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ngaytra': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tiendatcoc': forms.NumberInput(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'makhuyenmai': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mã khuyến mãi (nếu có)'}),
        }

    # cho mấy field này không bắt buộc
    ngaydat = forms.DateTimeField(required=False, widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}
    ))
    ngaynhan = forms.DateTimeField(required=False, widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}
    ))
    ngaytra = forms.DateTimeField(required=False, widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}
    ))
    tiendatcoc = forms.DecimalField(required=False)
    makhuyenmai = forms.IntegerField(required=False)
