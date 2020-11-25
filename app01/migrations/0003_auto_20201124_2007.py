# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-11-24 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20201124_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='contact_type',
            field=models.CharField(choices=[('0', 'qq'), ('1', '微信'), ('2', '手机')], default='0', max_length=16),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='source',
            field=models.CharField(choices=[('0', 'QQ群'), ('1', '51CTO'), ('2', '百度推广'), ('3', '知乎'), ('4', '转介绍'), ('5', '其他')], max_length=16),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='status',
            field=models.CharField(choices=[('0', '未报名'), ('1', '已报名'), ('2', '已退学')], max_length=16),
        ),
    ]
