"""supermarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from goods.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    # 上传部件自动调用的上传地址
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    # 用户模块URL
    url(r'^user/', include("user.urls", namespace="user")),
    # 商品模块URL
    url(r'^goods/', include("goods.urls", namespace="goods")),
    # 购物车模块
    url(r'^cart/', include("cart.urls", namespace="cart")),
    # 订单模块
    url(r'^order/', include("order.urls", namespace="order")),
    # 全文搜索框架
    url(r'^search/', include('haystack.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
