# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-12-03 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0016_menus_url_other_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Menus'),
        ),
    ]
