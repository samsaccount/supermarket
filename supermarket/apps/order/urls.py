from django.conf.urls import url

from order import views

urlpatterns = [
    url(r'^createAddr$', views.createAddr, name="creat_addr"),
    url(r'^addrManage$', views.addrManage, name="addr_manage"),
    url(r'^addrDel$', views.delAddr, name="addr_del"),
    url(r'^setDefault$', views.setDefault, name="setDefault"),
    url(r'^editAddr/(?P<id>\d+)/$', views.editAddr, name="edit_addr"),
    url(r'^confirm_order$', views.confirmOrder, name="confirm_order"),
    url(r'^show_order$', views.showOrder, name="show_order"),
    url(r'^pay$', views.pay, name="pay"),
    url(r'^success', views.success, name="success"),

]
