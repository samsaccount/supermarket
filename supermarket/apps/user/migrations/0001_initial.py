# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 07:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}', '手机号码格式错误')])),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3)),
                ('school', models.CharField(max_length=40, null=True)),
                ('hometown', models.CharField(max_length=40, null=True)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('avatar', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
