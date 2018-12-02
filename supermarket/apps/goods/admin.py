from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([GoodsSku,GoodsSpu,GoodsPic,Category,Unit,Banner,Events,EventsGoods,EventsPage])
# 每页显示条数
# list_per_page = 10
# # 在后端显示的字段
# list_display = ['id', 'name', 'brief', 'order', 'is_delete', 'create_time', 'update_time']
# # 给字段添加可编辑的a标签
# list_display_links = ['id', 'name']
# # 默认排序字段
# # ordering = ('-update_time')
# # 设置可编辑字段
# list_editable = ['brief', ]
# # 增加搜索框，可模糊查询
# search_fields = ['name', 'brief', 'order']
#
# 增加过滤器
# list_filter = ['name', 'is_delete']
# 时间分层筛选
# date_hierarchy = ['']
# 将多个字段放在一行
# fields = (("is_delete", "name"), "brief", "order", )
# 字段集合
# fieldsets = (
#     ("集合名称1", {"fields": ["字段名1", "字段名2"]}),
#     ("集合名称2", {"fields": ["字段名1", "字段名2"]}),
# )