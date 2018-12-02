# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_category_cate_order'),
        ('user', '0004_auto_20181120_1915'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('order_id', models.CharField(max_length=64, unique=True, verbose_name='订单编号')),
                ('order_cost', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='订单金额')),
                ('username', models.CharField(max_length=50, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='收货人电话')),
                ('addr', models.CharField(max_length=255, verbose_name='收货地址')),
                ('order_status', models.SmallIntegerField(choices=[(0, '待付款'), (1, '待发货'), (2, '已发货'), (3, '完成'), (4, '已评价'), (5, '申请退款'), (6, '已退款'), (7, '取消订单')], default=0, verbose_name='订单状态')),
                ('payfor', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='实付金额')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Payment', verbose_name='付款方式')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Transport', verbose_name='运输方式')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User', verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='OrderSku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('sku_num', models.IntegerField(verbose_name='商品数量')),
                ('sku_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='商品价格')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo', verbose_name='订单')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSku', verbose_name='sku_id')),
            ],
            options={
                'verbose_name': '订单商品表',
                'verbose_name_plural': '订单商品表',
            },
        ),
    ]
