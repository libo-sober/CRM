# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-12-03 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0015_menus_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='url_other_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
