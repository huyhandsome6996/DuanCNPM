from django import forms
from .models import DatPhong, KhachHang, CT_DatPhong, DichVu
from .services import check_booking_conflict

class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['hoten','cccd','sodt','email','diachi']

class DatPhongForm(forms.ModelForm):
    class Meta:
        model = DatPhong
        fields = ['khach','nhanvien','loaikhach','ngaynhan','ngaytra','ctv','ghichu']

    def clean(self):
        cleaned = super().clean()
        ngaynhan = cleaned.get('ngaynhan')
        ngaytra = cleaned.get('ngaytra')
        if ngaynhan and ngaytra and ngaytra < ngaynhan:
            raise forms.ValidationError("Ngày trả phải lớn hơn hoặc bằng ngày nhận.")
        # Không kiểm tra phòng ở đây (phòng ở CT_DatPhong)
        return cleaned

class CTDatPhongInlineForm(forms.ModelForm):
    class Meta:
        model = CT_DatPhong
        fields = ['phong','giaphong']

    def clean(self):
        cleaned = super().clean()
        phong = cleaned.get('phong')
        datphong = self.instance.datphong if self.instance.pk else None
        ngaynhan = self.initial.get('ngaynhan') or self.data.get('ngaynhan')
        ngaytra = self.initial.get('ngaytra') or self.data.get('ngaytra')
        # Use service check to validate conflict
        if phong and self.initial.get('ngaynhan') and self.initial.get('ngaytra'):
            conflict = check_booking_conflict(phong.id, self.initial['ngaynhan'], self.initial['ngaytra'])
            if conflict:
                raise forms.ValidationError("Phòng đã bị đặt trùng trong khoảng thời gian này.")
        return cleaned

class ChonDichVuForm(forms.Form):
    dichvu = forms.ModelChoiceField(queryset=DichVu.objects.filter(ngung=False))
    soluong = forms.IntegerField(min_value=1, initial=1)
