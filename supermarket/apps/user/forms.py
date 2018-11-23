from django import forms
from django.core.validators import RegexValidator
import hashlib

from user.helper import set_password
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
    # 验证两次密码是否一直
    def clean(self):
        data = self.cleaned_data
        phone = data.get("phone")
        password = data.get('password')
        Rpassword = data.get('Rpassword')
        num = User.objects.filter(phone=phone)
        if num:
            raise forms.ValidationError({"phone":"手机号已注册"})
        elif password != Rpassword:
            raise forms.ValidationError({"Rpassword": "两次密码不一致"})
        else:
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
    # 验证账户和密码是否正确
    def clean(self):
        data = self.cleaned_data
        phone = data.get("phone")
        password = data.get("password")
        password = set_password(password)
        num = User.objects.filter(phone=phone).first()
        if not num:
            raise forms.ValidationError({"phone": "请填写正确的账户和密码"})
        elif password != num.password:
            raise forms.ValidationError({"password": "请填写正确的账户和密码"})
        else:
            return data
