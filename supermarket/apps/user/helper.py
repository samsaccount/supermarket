import hashlib

from django.conf import settings
from django.shortcuts import redirect


def set_password(password):
    # 密码双重加密
    new_psd = "{}{}".format(password,settings.SECRET_KEY)
    h = hashlib.md5(new_psd.encode("utf-8"))
    return h.hexdigest()


def verify_login_required(func):
    # 登陆验证器
    def verify(request, *args, **kwargs):
        # 判断session中是否有ID,如果没有说明没有登录，请登录
        if request.session.get("is_Login") is None:
            # 配置文件中获取登录的URL地址
            login_url = settings.LOGIN_URL
            return redirect(login_url)
        else:
            # 返回被调用函数
            return func(request, *args, **kwargs)

    return verify
