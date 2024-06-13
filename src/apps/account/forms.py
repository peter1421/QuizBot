from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import SiteUser


class SiteUserCreationForm(UserCreationForm):
    # 使用自定義用戶模型
    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ( "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SiteUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control mb-0", "placeholder": "用戶名"},
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control mb-0", "placeholder": "密碼"},
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control mb-0", "placeholder": "確認密碼"},
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # 驗證電子郵件是否唯一
        if email and SiteUser.objects.filter(email=email).exists():
            raise forms.ValidationError("這個電子郵件已被註冊")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        # 驗證電話號碼是否唯一
        if SiteUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("這個電話號碼已被註冊")
        return phone


class SiteUserForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        model = SiteUser
        fields = ["username", "phone", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "請輸入用戶名"},
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "請輸入手機號碼"},
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "請輸入電子郵件地址"},
            ),
        }
