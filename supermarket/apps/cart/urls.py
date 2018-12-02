from django.conf.urls import url

from cart import views

urlpatterns = [
    url(r'^$', views.cart,name="cart"),
    url(r'^count$', views.cart_count,name="cart_count"),
]