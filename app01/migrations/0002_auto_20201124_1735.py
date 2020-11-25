# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-11-24 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('addr', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'verbose_name_plural': '校区',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.SmallIntegerField(choices=[(0, '脱产'), (1, '周末'), (2, '网络班')])),
                ('semester', models.SmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='毕业日期')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Branch')),
            ],
            options={
                'verbose_name_plural': '班级列表',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='课程名称')),
                ('price', models.PositiveSmallIntegerField()),
                ('period', models.PositiveSmallIntegerField(default=5, verbose_name='课程周期（月）')),
                ('outline', models.TextField(verbose_name='大纲')),
            ],
            options={
                'verbose_name_plural': '课程表',
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='课程节次')),
                ('title', models.CharField(max_length=64, verbose_name='本节主题')),
                ('content', models.TextField(verbose_name='本节内容')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework', models.TextField(blank=True, null=True, verbose_name='作业需求')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('class_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='上课班级')),
            ],
            options={
                'verbose_name_plural': '上课记录',
            },
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='跟踪内容')),
                ('status', models.SmallIntegerField(choices=[(0, '近期无报名计划'), (1, '一个月内报名'), (2, '2周内报名'), (3, '已报名')])),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '客户跟踪记录表',
            },
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=32)),
                ('contact_type', models.SmallIntegerField(choices=[(0, 'qq'), (1, '微信'), (2, '手机')], default=0)),
                ('contact', models.CharField(max_length=64, unique=True)),
                ('source', models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其他')])),
                ('consult_content', models.TextField(verbose_name='咨询内容')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')])),
                ('date', models.DateField(auto_now_add=True)),
                ('consult_courses', models.ManyToManyField(to='app01.Course', verbose_name='咨询课程')),
            ],
            options={
                'verbose_name_plural': '客户信息表',
            },
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='菜单名')),
                ('url_type', models.SmallIntegerField(choices=[(0, 'absolute'), (1, 'dynamic')], default=0)),
                ('url_name', models.CharField(max_length=128, verbose_name='连接')),
            ],
            options={
                'verbose_name_plural': '菜单',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('menus', models.ManyToManyField(blank=True, to='app01.Menus', verbose_name='菜单')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_grade', models.ManyToManyField(to='app01.ClassList')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.CustomerInfo')),
            ],
            options={
                'verbose_name_plural': '学员表',
            },
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (75, 'B-'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (0, 'N/A'), (-100, 'COPY')], default=0)),
                ('show_status', models.SmallIntegerField(choices=[(0, '缺勤'), (1, '已签到'), (2, '迟到'), (3, '早退')])),
                ('note', models.TextField(blank=True, null=True, verbose_name='成绩备注')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.CourseRecord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Student')),
            ],
            options={
                'verbose_name_plural': '学习记录',
            },
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '用户信息表'},
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=16, verbose_name='姓名'),
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together=set([('name', 'url_name')]),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='课程顾问'),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='referral_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.CustomerInfo', verbose_name='转介绍'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='跟进人'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='app01.UserInfo', verbose_name='讲师'),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('class_grade', 'day_num')]),
        ),
    ]
