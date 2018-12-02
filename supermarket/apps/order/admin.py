from django.contrib import admin

# Register your models here.
from order.models import UserAddress, Transport

admin.site.register(UserAddress)
admin.site.register(Transport)
