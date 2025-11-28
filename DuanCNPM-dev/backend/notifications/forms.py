from django import forms
from .models import ThongBao


class ThongBaoForm(forms.ModelForm):
    class Meta:
        model = ThongBao
        fields = ['tieude', 'noidung']
        widgets = {
            'tieude': forms.TextInput(attrs={'class': 'form-control'}),
            'noidung': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }
