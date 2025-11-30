from django import forms
from .models import DatPhong, CT_DatPhong, KhachHang, Phong, CongTacVien
LOAI_KHACH_CHOICES = [
    ('VANGLAI', 'Vãng lai'),
    ('TOUR_DOAN', 'Khách tour đoàn'),
    ('BOOKING', 'Booking'),
    ('AGODA', 'Agoda'),
    ('TRAVELOKA', 'Traveloka'),
]
class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['hoten', 'cccd', 'sodt', 'email', 'diachi']
        widgets = {
            'hoten': forms.TextInput(attrs={'class':'form-control'}),
            'cccd': forms.TextInput(attrs={'class':'form-control'}),
            'sodt': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'diachi': forms.TextInput(attrs={'class':'form-control'}),
        }
class CongTacVienForm(forms.ModelForm):
    class Meta:
        model = CongTacVien
        fields = ['hoten', 'sdt', 'zalo', 'ghichu']
        widgets = {
            'hoten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ tên cộng tác viên'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'zalo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zalo (nếu có)'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'placeholder': 'Ghi chú (nếu có)'}),
        }
        labels = {
            'hoten': 'Họ tên',
            'sdt': 'SĐT',
            'zalo': 'Zalo',
            'ghichu': 'Ghi chú',
        }
class DatPhongForm(forms.ModelForm):
    loaikhach = forms.ChoiceField(choices=LOAI_KHACH_CHOICES, required=True, label='Loại khách')
    class Meta:
        model = DatPhong
        fields = ['khach', 'nhanvien', 'loaikhach', 'ngaynhan', 'ngaytra', 'ctv', 'ghichu']
        widgets = {
            'khach': forms.Select(attrs={'class':'form-select'}),
            'nhanvien': forms.Select(attrs={'class':'form-select'}),
            'loaikhach': forms.Select(attrs={'class':'form-select'}),
            'ngaynhan': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'ngaytra': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'ctv': forms.Select(attrs={'class':'form-select'}),
            'ghichu': forms.Textarea(attrs={'class':'form-control','rows':2}),
        }

class CTDatPhongInlineForm(forms.ModelForm):
    class Meta:
        model = CT_DatPhong
        fields = ['phong', 'giaphong']
        widgets = {
            'phong': forms.Select(attrs={'class':'form-select'}),
            'giaphong': forms.NumberInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Nếu cần giới hạn phòng chỉ những phòng TRONG (mặc định)
        super().__init__(*args, **kwargs)
        self.fields['phong'].queryset = Phong.objects.filter(trangthai='TRONG').order_by('sophong')
