from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^reg$', views.reg, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^member$', views.member, name='member'),
    url(r'^user_info$', views.user_info, name='user_info'),
    url(r'^user_img$', views.UploadImg, name='upload'),
]
