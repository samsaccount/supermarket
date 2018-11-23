from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^reg$', views.reg, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^member$', views.member, name='member'),
    url(r'^records$', views.records, name='records'),
    url(r'^integral$', views.integral, name='integral'),
    url(r'^integral_exchange$', views.integral_exchange, name='integral_exchange'),
    url(r'^integral_records$', views.integral_records, name='integral_records'),
    url(r'^coupons$', views.coupons, name='coupons'),
    url(r'^coupons_overtime$', views.coupons_overtime, name='coupons_overtime'),
    url(r'^user_info$', views.user_info, name='user_info'),
    url(r'^user_img$', views.UploadImg, name='upload'),
]
