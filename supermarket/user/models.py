from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


class User(models.Model):
    choices = [(1, "男"), (2, "女"), (3, "保密")]
    phone = models.CharField(max_length=11,
                             validators=[RegexValidator(r'^1[3-9]\d{9}', "手机号码格式错误")],)
    nickname = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=50)
    sex = models.SmallIntegerField(choices=choices,default=3)
    school = models.CharField(max_length=40,null=True)
    hometown = models.CharField(max_length=40,null=True)
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    avatar = models.CharField(max_length=255,)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural= verbose_name
