# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-11-29 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20201125_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerfollowup',
            name='delete_status',
            field=models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')], default=0),
        ),
    ]