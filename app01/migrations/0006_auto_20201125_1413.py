# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-11-25 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20201125_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerinfo',
            name='consult_courses',
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='consult_courses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Course', verbose_name='咨询课程'),
        ),
    ]
