# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-12-03 05:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_auto_20201202_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]