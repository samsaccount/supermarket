from django import forms
from django.core.validators import RegexValidator

from order.models import UserAddress


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['hcity', 'hproper', 'harea', 'brief', 'username', 'phone', 'isDefault']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "brief": {
                "required": "详细地址必填"
            },
            "phone": {
                "required": "手机号码必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
        }

    def clean(self):
        # 验证当前用户的收货地址的数量,如果超过6个就报错
        user_id = self.data.get('user_id')
        count = UserAddress.objects.filter(user_id=user_id, is_delete=False).count()
        if count >= 6:
            raise forms.ValidationError("收货地址数量不能超过6")

        # 默认收货地址只能有一个, 判断当前添加的是否 isDefault==True,
        # 如果是就讲其他的收货地址都设置为False
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 如果是就讲其他的收货地址都设置为False
            UserAddress.objects.filter(user_id=user_id).update(isDefault=False)

        return self.cleaned_data


class AddressEditModelForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['hcity', 'hproper', 'harea', 'brief', 'username', 'phone', 'isDefault']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "brief": {
                "required": "详细地址必填"
            },
            "phone": {
                "required": "手机号码必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
        }

    def clean(self):
        user_id = self.data.get('user_id')

        # 默认收货地址只能有一个, 判断当前添加的是否 isDefault==True,
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 如果是就讲其他的收货地址都设置为False
            UserAddress.objects.filter(user_id=user_id).update(isDefault=False)

        return self.cleaned_data
