from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)
