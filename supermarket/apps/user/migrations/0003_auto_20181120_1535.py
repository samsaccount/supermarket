# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 07:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181119_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='images/memtx.png', max_length=200, upload_to='images/%Y/%m/%d', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hometown',
            field=models.CharField(max_length=40, null=True, verbose_name='老家'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=20, null=True, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=50, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}', '手机号码格式错误')], verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(max_length=40, null=True, verbose_name='学校'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
