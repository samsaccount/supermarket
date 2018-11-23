from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


class User(models.Model):
    choices = [(1, "男"), (2, "女"), (3, "保密")]
    phone = models.CharField(max_length=11,
                             validators=[RegexValidator(r'^1[3-9]\d{9}', "手机号码格式错误")],
                             verbose_name="手机")
    nickname = models.CharField(max_length=20, null=True, verbose_name="昵称")
    password = models.CharField(max_length=50, verbose_name="密码")
    sex = models.SmallIntegerField(choices=choices, default=3, verbose_name="性别")
    birthday = models.DateField(null=True, verbose_name="出生日期")
    local = models.CharField(null=True,max_length=200,verbose_name="当前位置")
    school = models.CharField(max_length=40, null=True, verbose_name="学校")
    hometown = models.CharField(max_length=40, null=True, verbose_name="老家")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateField(auto_now=True, verbose_name="修改时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    avatar = models.ImageField(max_length=200, upload_to="images/%Y/%m/%d", default="images/memtx.png",
                               verbose_name="头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
