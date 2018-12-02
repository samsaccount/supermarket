from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^detail/(?P<sku_id>\d+)/$', views.detail, name="detail"),
    url(r'^category/(?P<cate_id>\d+)/(?P<order_id>\d+)/$', views.category, name="category"),
]
