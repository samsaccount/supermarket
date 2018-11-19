from django import forms
from django.core.validators import RegexValidator
import hashlib
from user.models import User


class userReg(forms.Form):
    phone = forms.CharField(validators=[RegexValidator(r'^1[13456789]\d{9}$', "提示信息:手机号码格式错误")],
                            error_messages={
                                "required": "请填写手机号"
                            })
    password = forms.CharField(min_length=8, error_messages={
        "min_length": "请输入8位以上的密码",
        "required": "请填写密码"
    })
    Rpassword = forms.CharField(min_length=8, error_messages={
        "min_length": "请输入8位以上的密码",
        "required": "请填再次输入密码"
    })
    verif_code = forms.CharField(required=False, error_messages={
        "required": "请填写验证码"
    })
    # checkbox = forms.(attrs=True,)

    # 验证phone 是否已经注册过
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        num = User.objects.filter(phone=phone)
        if num:
            raise forms.ValidationError({"phone":"手机号已注册"})
        else:
            return phone

    # 验证两次密码是否一致
    def clean_Rpassword(self):
        data = self.cleaned_data
        if data.get('password') != data.get('Rpassword'):
            raise forms.ValidationError({"Rpassword": "两次密码不一致"})
        return data


class userLogin(forms.Form):
    phone = forms.CharField(validators=[RegexValidator(r'^1[13456789]\d{9}$', "提示信息:手机号码格式错误")],
                            error_messages={
                                "required": "请填写手机号"
                            })
    password = forms.CharField(min_length=8, error_messages={
        "min_length": "请输入8位以上的密码",
        "required": "请填写密码"
    })

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        num = User.objects.filter(phone=phone)
        if num == []:
            raise forms.ValidationError({"phone": "请填写正确的账户和密码"})
        else:
            return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        h = hashlib.md5(password.encode("utf-8"))
        password = h.hexdigest()
        num = User.objects.get(password=password)
        if password != num.password:
            raise forms.ValidationError({"password": "请填写正确的账户和密码"})
        else:
            return password
