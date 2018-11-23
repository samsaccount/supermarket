# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20181120_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(null=True, verbose_name='出生日期'),
        ),
        migrations.AddField(
            model_name='user',
            name='local',
            field=models.CharField(max_length=200, null=True, verbose_name='当前位置'),
        ),
    ]
