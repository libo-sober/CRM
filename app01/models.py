from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.


class UserInfo(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = '用户信息表'

    def __str__(self):  # __unicode__

        return self.username


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menus', verbose_name='菜单', blank=True)

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    """客户信息"""
    name = models.CharField(max_length=32, default=None, verbose_name='名称')
    contact_type_choices = (
        ('0', 'qq'),
        ('1', '微信'),
        ('2', '手机'),
    )
    contact_type = models.CharField(choices=contact_type_choices, default='0', max_length=16, verbose_name='联系方式')
    contact = models.CharField(max_length=64, unique=True, verbose_name='号码')

    source_choices = (
        ('0', 'QQ群'),
        ('1', '51CTO'),
        ('2', '百度推广'),
        ('3', '知乎'),
        ('4', '转介绍'),
        ('5', '其他'),
    )

    source = models.CharField(choices=source_choices, max_length=16, verbose_name='来源')
    referral_from = models.ForeignKey('self', null=True, blank=True, verbose_name='转介绍', on_delete=models.CASCADE)

    consult_courses = models.ForeignKey('Course', verbose_name='咨询课程', null=True, blank=True)
    consult_content = models.TextField(verbose_name='咨询内容')  # blank=True, null=True加上这个校验时就允许为空
    status_choices = (
        ('0', '未报名'),
        ('1', '已报名'),
        ('2', '已退学'),
    )
    status = models.CharField(choices=status_choices, max_length=16, verbose_name='状态')
    consultant = models.ForeignKey('UserInfo', verbose_name='课程顾问', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']  # 按id值倒序排列,等同于查询时customer_obj = models.CustomerInfo.objects.all().reverse() 注意后边加上了reverse()
        verbose_name_plural = '客户信息表'  # verbose_name会加上s,这个不hi

    def __str__(self):
        return self.name

    def show_status(self):
        # 设置每个状态的颜色
        status_color = {
            '0': 'blue',
            '1': 'green',
            '2': 'red',
        }
        return mark_safe(f"<span style='color:{status_color[self.status]}'>{self.get_status_display()}</span>")


class Student(models.Model):
    """学员表"""
    customer = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)

    class_grade = models.ManyToManyField('ClassList')

    class Meta:
        verbose_name_plural = '学员表'

    def __str__(self):
        return self.customer


class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey('CustomerInfo', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟踪内容')

    user = models.ForeignKey('UserInfo', verbose_name='跟进人', on_delete=models.CASCADE)
    status_choices = (
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2周内报名'),
        (3, '已报名'),
    )
    status = models.SmallIntegerField(choices=status_choices)
    delete_status_choices = (
        (0, '未删除'),
        (1, '已删除')
    )
    delete_status = models.SmallIntegerField(choices=delete_status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '客户跟踪记录表'

    def __str__(self):
        return self.customer.name + str(self.customer.id)


class Course(models.Model):
    """课程表"""
    name = models.CharField(verbose_name='课程名称', max_length=64, unique=True)
    price = models.PositiveSmallIntegerField()  # 必须为正
    period = models.PositiveSmallIntegerField(verbose_name='课程周期（月）', default=5)
    outline = models.TextField(verbose_name='大纲')

    class Meta:
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class_type_choices = (
        (0, '脱产'),
        (1, '周末'),
        (2, '网络班')
    )
    class_type = models.SmallIntegerField(choices=class_type_choices)
    semester = models.SmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserInfo', verbose_name='讲师')
    start_date = models.DateField('开班日期')
    graduate_date = models.DateField('毕业日期', blank=True, null=True)

    class Meta:
        verbose_name_plural = '班级列表'

    unique_together = (
        'course',
        'semester',
        'branch',
        'class_type',
    )

    def __str__(self):
        return '%s(%s)期' % (self.course.name, self.semester)


class CourseRecord(models.Model):
    """上课记录"""
    name = models.ForeignKey('CustomerInfo', verbose_name='姓名', default=None)
    class_grade = models.ForeignKey('ClassList', verbose_name='上课班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField('课程节次')
    teacher = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    title = models.CharField('本节主题', max_length=64)
    content = models.TextField('本节内容')
    has_homework = models.BooleanField('本节有作业', default=True)
    homework = models.TextField('作业需求', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '上课记录'
        unique_together = (
            'class_grade',
            'day_num',
        )

    def __str__(self):
        return '%s第(%s)节' % (self.class_grade, self.day_num)


class StudyRecord(models.Model):
    """学习记录"""

    course_record = models.ForeignKey('CourseRecord', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),  # not avaliable
        (-100, 'COPY'),
    )
    score = models.SmallIntegerField(choices=score_choices, default=0)
    show_choices = (
        (0, '缺勤'),
        (1, '已签到'),
        (2, '迟到'),
        (3, '早退'),
    )
    show_status = models.SmallIntegerField(choices=show_choices)
    note = models.TextField('成绩备注', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '学习记录'

    def __str__(self):
        return '%s %s %s' % (self.course_record, self.student, self.score)


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = '校区'

    def __str__(self):
        return self.name


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField('菜单名', max_length=32)

    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField('连接', max_length=128)

    class Meta:
        verbose_name_plural = '菜单'
        unique_together = ('name', 'url_name')

    def __str__(self):
        return self.name


class StudentEnrollment(models.Model):
    """
    学员报名表
    """
    why_us = models.CharField(verbose_name='为甚么加入', max_length=112)
    target = models.CharField(verbose_name='目标', max_length=112)
    customer = models.ForeignKey('CustomerInfo',on_delete=models.CASCADE, verbose_name='客户名',)
    class_grade = models.ForeignKey('ClassList',on_delete=models.CASCADE, verbose_name='班级',)
    consultant = models.ForeignKey('UserInfo',on_delete=models.CASCADE,verbose_name='跟进人')
    contract_agreed = models.BooleanField(default=False, verbose_name='审批状态',)
    contract_signed_date = models.DateTimeField(blank=True,null=True, verbose_name='合同签订日期', auto_now_add=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateTimeField('合同审核时间',blank=True,null=True, auto_now_add=True)

    class Meta:
        unique_together = ('customer','class_grade')
        verbose_name_plural = '报名表'

    def __str__(self):
        return '%s' % self.customer.name
