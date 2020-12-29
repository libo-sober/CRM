
@[TOC]

# Django项目：LOL学院学员管理系统

## 表结构设计

这里只涉及客户信息表及其相关的表，完整项目见文末链接。

```python
# models.py
from django.db import models
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

class CustomerInfo(models.Model):
    """客户信息"""
    name = models.CharField(max_length=32, default=None)
    contact_type_choices = (
        ('0', 'qq'),
        ('1', '微信'),
        ('2', '手机'),
    )
    contact_type = models.CharField(choices=contact_type_choices, default='0', max_length=16)
    contact = models.CharField(max_length=64, unique=True)

    source_choices = (
        ('0', 'QQ群'),
        ('1', '51CTO'),
        ('2', '百度推广'),
        ('3', '知乎'),
        ('4', '转介绍'),
        ('5', '其他'),
    )

    source = models.CharField(choices=source_choices, max_length=16)
    referral_from = models.ForeignKey('self', null=True, blank=True, verbose_name='转介绍', on_delete=models.CASCADE)

    consult_courses = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')
    status_choices = (
        ('0', '未报名'),
        ('1', '已报名'),
        ('2', '已退学'),
    )
    status = models.CharField(choices=status_choices, max_length=16)
    consultant = models.ForeignKey('UserInfo', verbose_name='课程顾问', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name

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
```

## 登录注册页面

自己可以去模板之家等网站扒一个自己喜欢的登录注册校验模板

login.html

```html
{% load static %}
<!DOCTYPE html>
<!-- saved from url=(0051)https://www.jq22.com/demo/jquery-Sharelink20151012/ -->
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>登陆</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
<div class="login-container">
    <h1>SuperCRM 登录页面</h1>
    <div class="connect">
        <p>欢迎来到LOL学院</p>
    </div>
    <form action="" method="post" id="loginForm"
          novalidate="novalidate">
        {% csrf_token %}
        <div>
            <input type="username" name="username" class="username" placeholder="用户名" oncontextmenu="return false"
                   onpaste="return false">
        </div>
        <div>
            <input type="password" name="password" class="password" placeholder="密码" oncontextmenu="return false"
                   onpaste="return false">
        </div>
        <button id="submit" type="submit">登 陆</button>
        <span style="color: red">{{ error }}</span>
    </form>
</div>
<a href="{% url 'register' %}">
    <button type="button" class="register-tis">还有没有账号？</button>
</a>
</div>

<script src="{% static 'js/jquery.min.js' %}"></script>
{#<script src="./登陆丨Sharelink_files/jquery.min.js(1).下载"></script>#}
<script src="{% static 'js/common.js' %}"></script>

<script src="{% static 'js/supersized.3.2.7.min.js' %}"></script>
<script src="{% static 'js/supersized-init.js' %}"></script>

<script src="{% static 'js/jquery.validate.min.js' %}"></script>

</body>
</html>
```

![image-20201125093900934](https://img-blog.csdnimg.cn/img_convert/3495889ffbee66e3404cb72e3e511523.png)



注册页面

```html
{% load static %}
<!DOCTYPE html>
<!-- saved from url=(0064)https://www.jq22.com/demo/jquery-Sharelink20151012/register.html -->
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>登陆</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
<div class="register-container">
    <h1>ShareLink</h1>
    <div class="connect">
        <p style="left: 0%;">Link the world. Share to world.</p>
    </div>
    <form action="" method="post" id="registerForm"
          novalidate="novalidate">
    {% csrf_token %}
        {% for field in register_form_obj %}
            <div>
{#                <label for="{{ field.id_for_label }}">{{ field.label }}</label>#}
                {{ field }}
                <span style="color: red;">{{ field.errors.0 }}</span>
            </div>
        {% endfor %}
        <button id="submit" type="submit">注 册</button>
    </form>
    <a href="{% url 'login' %}">
        <button type="button" class="register-tis">已经有账号？</button>
    </a>
</div>

<script src="{% static 'js/jquery.min.js' %}"></script>
{#<script src="./登陆丨Sharelink_files/jquery.min.js(1).下载"></script>#}
<script src="{% static 'js/common.js' %}"></script>

<script src="{% static 'js/supersized.3.2.7.min.js' %}"></script>
<script src="{% static 'js/supersized-init.js' %}"></script>

<script src="{% static 'js/jquery.validate.min.js' %}"></script>
</body>
</html>
```

![image-20201125093932101](https://img-blog.csdnimg.cn/img_convert/40c15b8ff7a7c8bb3a1ea132473a0d5d.png)

## 登录处理视图逻辑和URL

```python
# views.py
import re

from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.core.exceptions import ValidationError
from django.views import View
from django import forms

from app01 import models
from app01.utils.hashlib_func import set_md5
from app01.utils.page_html import MyPagination
# Create your views here.


# 自定义验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  # 自定义验证规则的时候，如果不符合你的规则，需要自己发起错误


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=6,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class': 'username', 'autocomplete': 'off', 'placeholder': '用户名', }),
        error_messages={
            'required': '用户名不能为空！',
            'max_length': '用户名不能大于16位！',
            'min_length': '用户名不能小于6位！',
        }
    )

    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '密码', 'oncontextmenu': 'return false', 'onpaste': 'return false', }),
        error_messages={
            'required': '密码不能为空！',
            'max_length': '密码不能大于16位！',
            'min_length': '密码不能小于6位！',
        }
    )

    r_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(attrs={'class': 'password', 'placeholder': '请再次输入密码', }),
        error_messages={
            'required': '密码不能为空！',
        }
    )

    # 全局钩子
    def clean(self):
        values = self.cleaned_data
        r_password = values.get('r_password')
        password = values.get('password')
        if password == r_password:
            return values
        else:
            self.add_error('r_password', '两次输入的密码不一致！')

    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'invalid': '邮箱格式不对！',
            'required': '邮箱不能为空！',
        },
        widget=forms.widgets.EmailInput(attrs={'class': 'email', 'placeholder': '输入邮箱地址', 'type': 'email'}),
        # validators=[],
    )

    telephone = forms.CharField(
        label='手机号',
        error_messages={
            'required': '手机号不能为空！',
        },
        widget=forms.widgets.TextInput(attrs={'class': 'phone_number', 'placeholder': '请输入手机号', }),
        validators=[mobile_validate, ],
    )


class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
        if user_obj:
            # return HttpResponse('ok')
            return redirect('home')
        else:
            # return redirect('login')
            return render(request, 'login.html', {'error': '用户名或密码错误！'})


class RegisterView(View):

    def get(self, request):
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})

    def post(self, request):
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            password = register_form_obj.cleaned_data.pop('password')
            password = set_md5(password)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(
                **register_form_obj.cleaned_data
            )
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})
# urls.py
from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'^home/', views.HomeView.as_view(), name='home'),
    url(r'^customer/', views.CustomerView.as_view(), name='customer'),
]
```

## 批量插入LOL英雄信息

**插入数据**

1. 进入admin后台添加
2. 在views.py中手动添加
3. MySQL数据库添加
4. navicat添加
5. django项目下直接创建py文件批量添加

方法5：create_table_bats.py

```python
import os
import random

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modelform.settings")
    import django
    django.setup()
    from app01 import models
    names = []
    with open('statics/plugins/lol_name', 'r', encoding='utf-8') as f:
        for line in f:
            names.append(line.strip())
    print(len(names))
    customer_obj = []
    for i in range(100, 180):

        obj = models.CustomerInfo(
            name=names[i-100],
            contact_type=random.randint(0, 2),
            contact=f'21321378{i}',
            source=random.randint(0, 5),
            referral_from_id=models.CustomerInfo.objects.get(id=1).id,
            consult_courses_id=models.Course.objects.get(id=1).id,
            consult_content='什么是'+names[i-100]+'?',
            status=random.randint(0, 2),
            consultant_id=models.UserInfo.objects.get(id=1).id
        )
        customer_obj.append(obj)
    models.CustomerInfo.objects.bulk_create(customer_obj)
```

## 英雄信息主页

自己去GitHub上下载一个AdminLTE后台管理系统，然后修改加进来。

starter.html

```html
# 修改AdminLTE中starter,html
# 并copy相应用到的js、css文件到项目静态文件夹下，配置静态路径
# 把相关js、css文件引入html文件
```

home.html

```html
{% extends 'starter.html' %}

{% block content %}
    <table class="table table-hover table-bordered">
    <thead>
    <tr>
        <td>序号</td>
        <td>姓名</td>
        <td>联系方式</td>
        <td>号码</td>
        <td>来源</td>
        <td>转介绍人员</td>
        <td>状态</td>
        <td>课程顾问</td>
        <td>咨询日期</td>
        <td>咨询内容</td>
    </tr>
    </thead>
    <tbody>
        {% for customer in customer_obj %}
            <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ customer.name }}</td>
        <td>{{ customer.get_contact_type_display }}</td>
        <td>{{ customer.contact }}</td>
        <td>{{ customer.get_source_display }}</td>
        <td>{{ customer.referral_from.name }}</td>
        <td>{{ customer.get_status_display }}</td>
        <td>{{ customer.consultant.username }}</td>
        <td>{{ customer.date }}</td>
        <td>{{ customer.consult_content }}</td>
            </tr>
        {% endfor %}
    </tbody>
    </table>

{% endblock content %}
```

![image-20201125094248792](https://img-blog.csdnimg.cn/img_convert/867811f643dfba1b4ad66b559175409c.png)

## 英雄信息分页

**views.py中**

```python
class CustomerView(View):

    def get(self, request):
        page_id = request.GET.get('page') # 获取get请求中的page数据
        num = models.CustomerInfo.objects.all().count()
        page_num = 15
        a, b = divmod(num, page_num)
        page = a if b else a
        page_count = 9
        mid = page_count // 2
        if page_id is None:
            page_id = 1
        else:
            page_id = int(page_id)
        if page_id < mid:
            page_num_list = range(1,page_count+1)
        else:
            page_num_list = range(page_id - mid, page_id + mid + 1)  
        customer_obj = models.CustomerInfo.objects.all()[(page_id - 1) * page_num:page_id * page_num]
        # print(page_id)
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_num_list': page_num_list, })
```

**customer.html**

```html
{% extends 'starter.html' %}
{% load static %}
{% block content %}
    <table class="table table-hover table-bordered">
        <thead>
        <tr>
            <td>序号</td>
            <td>姓名</td>
            <td>联系方式</td>
            <td>号码</td>
            <td>来源</td>
            <td>转介绍人员</td>
            <td>状态</td>
            <td>课程顾问</td>
            <td>咨询日期</td>
            <td>咨询内容</td>
        </tr>
        </thead>
        <tbody>
        {% for customer in customer_obj %}
            <tr>
                {#        <td>{{ forloop.counter }}</td>#}
                <td>{{ customer.id }}</td>
                <td>{{ customer.name }}</td>
                <td>{{ customer.get_contact_type_display }}</td>
                <td>{{ customer.contact }}</td>
                <td>{{ customer.get_source_display }}</td>
                <td>{{ customer.referral_from.name }}</td>
                <td>{{ customer.get_status_display }}</td>
                <td>{{ customer.consultant.username }}</td>
                <td>{{ customer.date }}</td>
                <td>{{ customer.consult_content }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    <div class="container">
    <div class="row">
    <div class="row-cols-8 offset-2">
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <li>
                <a href="#" aria-label="Previous">
                    <span style="font-size: 25px" aria-hidden="true">&laquo;</span>
                </a>
            </li>
            {% for i in page_num_list %}
                <li style="font-size: 25px"><a href="/customer/?page={{ i }}"> {{ i }} &nbsp;</a></li>
            {% endfor %}
            <li>
                <a href="#" aria-label="Next">
                    <span style="font-size: 25px" aria-hidden="true">&raquo;</span>
                </a>
            </li>
        </ul>
    </nav>
    </div>
    </div>
    </div>
{% endblock content %}
```

<img src="https://i.loli.net/2020/11/25/yfIc4pSvBrJM6nl.png" alt="image-20201125165406070" style="zoom:150%;" />

## 封装分页功能

app01/utils/page_html

```python
from django.utils.safestring import mark_safe


class MyPagination:

    def __init__(self, page_id, num, base_url, page_count=9, record=15):
        a, b = divmod(num, record)
        page = a + 1 if b else a  # 这些记录可以分多少页
        mid = page_count // 2
        if page_id is None:
            page_id = 1
        else:
            page_id = int(page_id)
        if page_id <= mid:
            page_num_list = range(1, page_count + 1)
        elif page_id > page - mid:
            page_num_list = range(page - page_count + 1, page + 1)
        else:
            page_num_list = range(page_id - mid, page_id + mid + 1)
        self.page_id = page_id
        self.num = num
        self.page = page
        self.page_num_list = page_num_list
        self.record = record
        self.base_url = base_url

    @property
    def get_record(self):
        return self.record

    @property
    def get_page_id(self):
        return self.page_id

    def html_page(self):
        page_html = '<div class="container"><div class="row"><div class="row-cols-8 offset-2"><nav aria-label="Page navigation"><ul class="pagination">'

        if self.page_id <= 1:
            page_pre = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        else:
            page_pre = f'<li><a href="{self.base_url}?page={self.page_id - 1}" aria-label="Previous"><span style="font-size: 25px" aria-hidden="true">&laquo;</span></a></li>'
        page_html += page_pre
        for i in self.page_num_list:
            if i == self.page_id:
                page_html += f'<li class="active" style="font-size: 25px"><a href="{self.base_url}?page={i}"> {i} </a></li>'
            else:
                page_html += f'<li style="font-size: 25px"><a href="{self.base_url}?page={i}"> {i} </a></li>'
        if self.page_id >= self.page:
            page_last = f'<li class="disabled"><a href="javascript:void(0)" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        else:
            page_last = f'<li><a href="{self.base_url}?page={self.page_id + 1}" aria-label="Next"><span style="font-size: 25px" aria-hidden="true">&raquo;</span></a></li>'
        page_html += page_last
        page_html += '</ul></nav></div></div></div>'
        # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签
        return mark_safe(page_html)

```

views.py

```python
from modelform import settings


class CustomerView(View):

    def get(self, request):
        page_id = request.GET.get('page') # 获取get请求中的page数据
        num = models.CustomerInfo.objects.all().count()  # 总共记录数
        base_url = request.path  # 请求路径
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        # print(base_url)

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, page_count=page_count, record=record)

        customer_obj = models.CustomerInfo.objects.all()[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        # print(page_id)
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_html': html_obj.html_page(), })
```

settings.py

```python
PAGE_COUNT = 9  # 页数栏显示多少个数
RECORD = 15  # 每页显示多少条记录
```

customer.html

```python
{% extends 'starter.html' %}
{% load static %}
{% block content %}
    <table class="table table-hover table-bordered">
        <thead>
        <tr>
            <td>序号</td>
            <td>姓名</td>
            <td>联系方式</td>
            <td>号码</td>
            <td>来源</td>
            <td>转介绍人员</td>
            <td>状态</td>
            <td>课程顾问</td>
            <td>咨询日期</td>
            <td>咨询内容</td>
        </tr>
        </thead>
        <tbody>
        {% for customer in customer_obj %}
            <tr>
                {#        <td>{{ forloop.counter }}</td>#}
                <td>{{ customer.id }}</td>
                <td>{{ customer.name }}</td>
                <td>{{ customer.get_contact_type_display }}</td>
                <td>{{ customer.contact }}</td>
                <td>{{ customer.get_source_display }}</td>
                <td>{{ customer.referral_from.name }}</td>
                <td>{{ customer.get_status_display }}</td>
                <td>{{ customer.consultant.username }}</td>
                <td>{{ customer.date }}</td>
                <td>{{ customer.consult_content }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
{#    自己封装的分页组件#}
{#    {{ page_html|safe }}#}
{#     # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签#}
    {{ page_html }}
{% endblock content %}
```

![image-20201125203848591](https://img-blog.csdnimg.cn/img_convert/87132e77d77434128abfadcbdf76934b.png)

## 添加和编辑英雄信息

```python
# 两个表完全可以合一
# 编辑和添加用户
class AddEditCustomer(View):

    def get(self, request, cid=None):
        label = '编辑客户' if cid else '添加客户'
        customer_obj= models.CustomerInfo.objects.filter(pk=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
        customer_form = CustomerForm(instance=customer_obj)
        return render(request, 'add_customer.html', {'customer_form':customer_form, 'label':label})

    def post(self, request, cid=None):
        label = '编辑客户' if cid else '添加客户'
        customer_obj = models.CustomerInfo.objects.filter(pk=cid).first()
        customer_form = CustomerForm(request.POST, instance=customer_obj)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('customer')
        else:
            return render(request, 'add_customer.html', {'customer_form': customer_form, 'label':label})
# url
    url(r'^add_customer/', views.AddEditCustomer.as_view(), name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.AddEditCustomer.as_view(), name='edit_customer'),
```

## 预留钩子动态生成页面标题

starter.html

```html
<div class="col-sm-6">
  <h1 class="m-0 text-dark">
      {% block son_content %}
      LOL学员信息
      {% endblock %}
  </h1>
</div><!-- /.col -->
```

add_customer.html，编辑页面也使用此页面，label在views中动态传输

```python
{% block son_content %}
    {{ label }}
{% endblock %}
# views
label = '编辑客户' if cid else '添加客户'
```

## 控制不同状态显示不同颜色

客户信息表中增加此方法：

```python
def show_status(self):
    # 设置每个状态的颜色
    status_color = {
        '0': 'blue',
        '1': 'green',
        '2': 'red',
    }
    return mark_safe(f"<span style='color:{status_color[self.status]}'>{self.get_status_display()}</span>")
```

在显示页面customer.html文件中调用

```python
<td>{{ customer.show_status }}</td>
# 不同报名状态显示不同颜色
```

![image-20201125215536060](https://img-blog.csdnimg.cn/img_convert/2f6267b9cf88e5f00fd36971aef9a385.png)

## 动态生成验证码

使用的是pillow模块动态画图，然后随机画数字，最后随机加噪点。

建议想加入验证码的直接在登陆注册验证时去模板之家扒一个带滑块验证的即可。

## 按条件搜索和保存搜索条件

**对原先的CustomerView进行升级**

```python
class CustomerView(View):

    def get(self, request):

        # print(request.GET.urlencode())  # 会直接拿到get请求根路径后边的url
        # request.GET 拿到的是一个QuerrySet不允许修改
        # 先不进行urlecode,因为后边会多出一个page
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        print(get_data)
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        search_field = request.GET.get('search_field')  # 获取get请求中的搜索字段
        search = request.GET.get('search')  # 获取get请求中的搜索数据
        contact_type_choices = {
            'qq':'0',
            '微信':'1',
            '手机':'2',
        }
        if search_field == 'contact_type__contains':
            search = contact_type_choices[search]
        # print(search_field, search)
        if search:
            #1. Q查询实现多条件查询，或者关系
            # customer_obj_list = models.CustomerInfo.objects.filter(Q(name__contains=search) | Q(contact__contains=search))
            # 2.**打散,and关系
            # customer_obj_list = models.CustomerInfo.objects.filter(**{search_field:search})
            # 3.Q的另一种方式, q_obj.connector = 'or',  不加or就是and关系
            q_obj = Q()
            # q_obj.connector = 'or'
            q_obj.children.append((search_field, search))
            # q_obj.children.append((search_field2, search2)) 同时用连个条件查询
            customer_obj_list = models.CustomerInfo.objects.filter(q_obj)
        else:
            customer_obj_list = models.CustomerInfo.objects.all()

        num = customer_obj_list.count()  # 总共记录数
        print(num)
        base_url = request.path  # 请求路径
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        # print(base_url)

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        customer_obj = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        # print(page_id)
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_html': html_obj.html_page(), })
```

**动态生成携带搜索条件的get请求分页链接**

```python
# page_html.py
# 动态生成page
for i in self.page_num_list:
    self.get_data['page'] = i  # 把发来的page动态生成
    if i == self.page_id:
        page_html += f'<li class="active" style="font-size: 25px"><a href="{self.base_url}?{self.get_data.urlencode()}"> {i} </a></li>'
    else:
        page_html += f'<li style="font-size: 25px"><a href="{self.base_url}?{self.get_data.urlencode()}"> {i} </a></li>'
```

![image-20201126151910992](https://img-blog.csdnimg.cn/img_convert/ce2bfc34d192b9538e67374f843716e7.png)

## 公私分户

公私户走同一个视图函数处理

```python
url(r'^customer/', views.CustomerView.as_view(), name='customer'),
url(r'^my_customer/', views.CustomerView.as_view(), name='my_customer'),
```

在loginview中添加当前登录用户的id并存入session中

```python
class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
        if user_obj:
            # return HttpResponse('ok')
            # 把当前用户id添加到session中
            request.session['user_id'] = user_obj.id
            return redirect('home')
        else:
            # return redirect('login')
            return render(request, 'login.html', {'error': '用户名或密码错误！'})
```



customerview中只需加上请求路径公私户判别，和获取session的user_id后进行结果筛选即可，其余不变。

```python
class CustomerView(View):

    def get(self, request):

        # print(request.GET.urlencode())  # 会直接拿到get请求根路径后边的url
        # request.GET 拿到的是一个QuerrySet不允许修改
        # 先不进行urlecode,因为后边会多出一个page
        get_data = request.GET.copy()  # 直接调用这个类自己的copy方法或者deepcopy方法或者自己import copy 都可以实现内容允许修改
        user_id = request.session.get('user_id')
        cur_user_name = models.UserInfo.objects.get(id=user_id)
        # print(user_id)
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        search_field = request.GET.get('search_field')  # 获取get请求中的搜索字段
        search = request.GET.get('search')  # 获取get请求中的搜索数据
        contact_type_choices = {
            'qq':'0',
            '微信':'1',
            '手机':'2',
        }
        if search_field == 'contact_type__contains':
            if search in ['qq', '微信', '手机']:
                search = contact_type_choices[search]
        # print(search_field, search)
        cur_request_path = request.path
        if cur_request_path == reverse('my_customer'):
            cur_user_customer = models.CustomerInfo.objects.filter(consultant_id=user_id)
        else:
            cur_user_customer = models.CustomerInfo.objects.filter(consultant_id__isnull=True)

        if search:
            #1. Q查询实现多条件查询，或者关系
            # customer_obj_list = models.CustomerInfo.objects.filter(Q(name__contains=search) | Q(contact__contains=search))
            # 2.**打散,and关系
            # customer_obj_list = models.CustomerInfo.objects.filter(**{search_field:search})
            # 3.Q的另一种方式, q_obj.connector = 'or',  不加or就是and关系
            q_obj = Q()
            # q_obj.connector = 'or'
            q_obj.children.append((search_field, search))
            # q_obj.children.append((search_field2, search2)) 同时用连个条件查询
            customer_obj_list = cur_user_customer.filter(q_obj)
        else:
            customer_obj_list = cur_user_customer.all()

        num = customer_obj_list.count()  # 总共记录数
        print(num)
        base_url = request.path  # 请求路径
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        # print(base_url)

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        customer_obj = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        # print(page_id)
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name})
```

## 公私互转

在get中发了一个tag标签，处于公户情况下只能公转私，否则私转公

customer.html

```html
<form class="form-inline pull-left" method="post">
{% csrf_token %}
    <select name="gs_sg" class="form-control">
        {% if tag == 'gs' %}
        <option value="reverse_gs">公户转私户</option>
        {% else %}
        <option value="reverse_sg">私户转公户</option>
        {% endif %}
    </select>

    <button class="btn btn-warning">go</button>


    <table class="table table-hover table-bordered">
        <thead>
        <tr>
            <td><input type="checkbox">选择</td>
            <td>序号</td>
            <td>姓名</td>
            <td>联系方式</td>
            <td>号码</td>
            <td>来源</td>
            <td>转介绍人员</td>
            <td>状态</td>
            <td>课程顾问</td>
            <td>咨询日期</td>
            <td>咨询内容</td>
            <td>操作</td>
        </tr>
        </thead>
        <tbody>
        {% for customer in customer_obj %}

            <tr>
                <td><input type="checkbox" value="{{ customer.id }}" name="customer_ids"></td>
                <td>{{ forloop.counter }}</td>
                {#                <td>{{ customer.id }}</td>#}
                <td>{{ customer.name }}</td>
                <td>{{ customer.get_contact_type_display }}</td>
                <td>{{ customer.contact }}</td>
                <td>{{ customer.get_source_display }}</td>
                <td>{{ customer.referral_from.name|default:'无' }}</td>
                <td>{{ customer.show_status }}</td>
                <td>{{ customer.consultant.username|default:'无' }}</td>
                <td>{{ customer.date }}</td>
                <td>{{ customer.consult_content }}</td>
                <td><a href="{% url 'edit_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>
            </tr>

        {% endfor %}
        </tbody>
    </table>
    {#    自己封装的分页组件#}
    {#    {{ page_html|safe }}#}
    {#     # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签#}
    {{ page_html }}
</form>
```

CustomerView中增加post方法来处理这个请求

```python
def post(self, request):
    print(request.POST)
    gs_sg = request.POST.get('gs_sg')
    customer_ids = request.POST.getlist('customer_ids')
    if hasattr(self, gs_sg):
        res_obj = models.CustomerInfo.objects.filter(pk__in=customer_ids)
        getattr(self, gs_sg)(request, res_obj)
        return redirect(request.path)
```

![image-20201126204132420](https://img-blog.csdnimg.cn/img_convert/6e793f89b8844290d5718764651b6eb5.png)

## 自定义中间件利用session登陆认证和登出逻辑

loginmiddleware.py

```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from app01 import models


class MyLoginAuth(MiddlewareMixin):

    def process_request(self, request):
        # 白名单
        white_list = [reverse('login'), reverse('register'), ]
        if request.path in white_list:
            return
        user_id = request.session.get('user_id')
        # print(user_id)
        if user_id:
            # 将当前登录用户对象封装到request类中，成为它的一个属性，这样就可以在后边的request中直接使用
            request.user_obj = models.UserInfo.objects.get(id=user_id)
            return

        else:
            return redirect('login')
```

settings里配置你的中间件

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    'app01.utils.loginmiddleware.MyLoginAuth',
]
```

现在就可以进行登录认证了，后边加一个登出逻辑，就是点击登出，清楚所有cookie和session

```python
# 登出视图逻辑
class LoginOutView(View):

    def get(self, request):
        request.session.flush()  # 清楚所有的cookie和session
        return redirect('login')

    
# url路由
url(r'^home/', views.HomeView.as_view(), name='home'),
```

## 跳转回源路径和url编码

  点击完编辑后会直接跳转到/customer/路径 不会回到你编辑是那个?page=3,所以要解决这个问题。但是，用get_full_path获取路径时，带有搜索条件的&kw=111&name_contains=11这些会根据&断开取关键字，这是由url编码格式决定的。为了解决这个问题，引入QueryDict类，使用它的urlencode()方法。它会在编码时把特殊字符按照ASCII码对应的十六进制字符替换掉，这样在url编码时就不出现之前的关键字断开了。

   此时，我们需要在请求时的url上添加提交后要去的路径。原来的url反向解析已经不能满足我们的需求，借助自定义标签来拼接href路径。

my_tags.py

```python
from django.urls import reverse
from django import template
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag
def resolve_url(request, url_name, pk):
    next_url = request.get_full_path()
    # print(next_url)  # /customer/
    destination = reverse(url_name, args=(pk,))
    qd =QueryDict(mutable=True)  # mutable 可不可变，默认是False
    qd['next'] = next_url
    full_url = destination + '?' + qd.urlencode()  # /edit_customer/723/?next=%2Fcustomer%2F%3Fpage%3D2 按照ascii码十六进制替换/ ？ &
    # /edit_customer/703/?next=/customer/?search_field=contact__contains&search=8&page=4
    # /edit_customer/703/?next=%2Fcustomer%2F%3Fsearch_field%3Dcontact__contains%26search%3D8%26page%3D4
    # 不用urlencode会导致在带有搜索条件的查询时，在后端request.get不到完整的？后变的信息
    # full_url = destination + '?next=' + next_url  # /edit_customer/714/?next=/customer/?page=2
    print(full_url)
    return full_url
```

customer.html中的编辑标签的href属性值中使用自定义的标签，

```html
<td><a href="{% resolve_url request 'edit_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>
```

会返回携带next_url的一个完整路径：

```
/edit_customer/703/?next=%2Fcustomer%2F%3Fsearch_field%3Dcontact__contains%26search%3D8%26page%3D4
```

，这是经过urlencode之后的，之前的路径就是：

```
/edit_customer/703/?next=/customer/?search_field=contact__contains&search=8&page=4
```

携带下一个返回时的url进入编辑页面时，在edit页面发起post请求后在editview中处理post请求信息后重定向到此时的request对象中的next对应的路径值即可。

就是：

```
%2Fcustomer%2F%3Fsearch_field%3Dcontact__contains%26search%3D8%26page%3D4
```

源路径

```
/customer/?search_field=contact__contains&search=8&page=4
```

## 跟进记录以及其分页和搜索

很简单了，就根据客户的逻辑进行修改。

```python
# 跟进记录
class FollowCustomerView(View):

    def get(self, request):
        get_data = request.GET.copy()
        cur_user_name = request.user_obj.username
        cid = request.GET.get('cid')
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        search_field = request.GET.get('search_field')  # 获取get请求中的搜索字段
        search = request.GET.get('search')  # 获取get请求中的搜索数据
        # print(search)
        # print(cid)
        if cid:
            cur_follow_customer = models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0, customer_id=cid)
        else:
            cur_follow_customer = models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0)
        if search:
            q_obj = Q()
            q_obj.children.append((search_field, search))
            customer_obj_list = cur_follow_customer.filter(q_obj)
        else:
            customer_obj_list = cur_follow_customer.all()

        num = customer_obj_list.count()  # 总共记录数
        # print(num)
        base_url = request.path  # 请求路径
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        follow_customer = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        return render(request, 'follow_customer.html', {'follow_customer': follow_customer, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name,})

    def post(self, request):

        print(request.POST)
        customer_ids = request.POST.getlist('customer_ids')
        models.CustomerFollowUp.objects.filter(customer_id__in=customer_ids).delete()

        return redirect(request.path)
    
    
# urls
# 跟进记录
url(r'^follow_customer/', MyCustomer.FollowCustomerView.as_view(), name='follow_customer'),
```

follow_customer.html

```html
{% extends 'starter.html' %}
{% load static %}

{% block username %}
    {{ request.user_obj.username }}
{% endblock %}

{% block content %}
    <h3><a href="{% url 'add_follow_customer' %}">添加跟进客户</a></h3>
    {% load my_tags %}

    <form method="get" class="form-inline pull-right">
        <select name="search_field" class="form-control">
            <option value="customer__name__contains">客户名</option>
            <option value="customer__name__contains">跟进人</option>
        </select>
        <div class="form-group">
            <input type="text" class="form-control" name="search" placeholder="请输入搜索的内容">
        </div>
        <button type="submit" class="btn btn-default">搜索</button>
    </form>
    <form class="form-inline pull-left" method="post">
    {% csrf_token %}
            <select name="delete_follow_customer" class="form-control">
<option value="delete_all">删除</option>
        </select>

        <button class="btn btn-warning">go</button>

        <table class="table table-hover table-bordered">
            <thead>
            <tr>
 <td><input type="checkbox">选择</td>
                <td>序号</td>
                <td>姓名</td>
                <td>跟进内容</td>
                <td>跟进人</td>
                <td>状态</td>
                <td>跟进日期</td>
                <td>操作</td>
            </tr>
            </thead>
            <tbody>
            {% for customer in follow_customer %}

                <tr>
                <td><input type="checkbox" value="{{ customer.customer.id }}" name="customer_ids"></td>
                    <td>{{ forloop.counter }}</td>
                    {#                <td>{{ customer.id }}</td>#}
                    <td>{{ customer.customer }}</td>
                    <td>{{ customer.content }}</td>
                    <td>{{ customer.user.username }}</td>
                    <td>{{ customer.get_status_display }}</td>
                    <td>{{ customer.date }}</td>
{#                    <td><a href="{% url 'edit_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>#}
{#                    <td><a href="{% resolve_url request 'add_follow_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>#}
                    <td><a href="{% resolve_url request 'edit_follow_customer' customer.customer.id %}"><i class="fa fa-edit"></i></a></td>
                </tr>

            {% endfor %}
            </tbody>
        </table>
        {#    自己封装的分页组件#}
        {#    {{ page_html|safe }}#}
        {#     # mark_safe()后端包裹后，前端就不要safe过滤了，自动识别成标签#}
        {{ page_html }}
    </form>
{% endblock content %}
```

## 编辑和添加跟进记录

```python
# 跟进客户modelform
class FollowCustomerForm(forms.ModelForm):

    class Meta:
        model = models.CustomerFollowUp
        fields = '__all__'
        exclude = ['delete_status', ]


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # modelform默认会生成这个外键关联的表的所有信息，就是models.CustomerInfo.objects.all()
            # 我们只想显示当前用户下的客户信息
            if field_name == 'customer':
                field.queryset = models.CustomerInfo.objects.filter(consultant=request.user_obj)
            elif field_name == 'user':
                field.choices = ((request.user_obj.id, request.user_obj.username),)

# 添加和编辑跟进客户信息
class AddEditFollowCustomerView(View):

    def get(self, request, cid=None):
        label = '编辑跟进客户' if cid else '添加跟进客户'
        follow_customer_obj= models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0, customer_id=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
        # print(follow_customer_obj, cid)
        follow_customer_form = FollowCustomerForm(request, instance=follow_customer_obj)
        return render(request, 'add_follow_customer.html', {'follow_customer_form':follow_customer_form, 'label':label})

    def post(self, request, cid=None):
        label = '编辑跟进客户' if cid else '添加跟进客户'
        follow_customer_obj = models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0, customer_id=cid).first()
        follow_customer_form = FollowCustomerForm(request.POST, instance=follow_customer_obj)
        next_url = request.GET.get('next')
        # print(next_url)
        if follow_customer_form.is_valid():
            follow_customer_form.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('follow_customer')
        else:
            return render(request, 'add_customer.html', {'follow_customer_form': follow_customer_form, 'label':label})
```

add_follow_customer.html

```html
{% extends 'starter.html' %}

{% block son_content %}
    {{ label }}
{% endblock %}

{% block content %}
    <form class="form-horizontal" method="post" novalidate>
    {% csrf_token %}
        {% for field in follow_customer_form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}" class="col-sm-2 control-label">{{ field.label }}</label>
                <div class="col-sm-6">
                    {{ field }}
                </div>
                <div class="col-sm-4">
                    <span style="color: red">{{ field.errors.0 }}</span>
                </div>
            </div>
        {% endfor %}
    <div class="col-sm-6 offset-8">
        <button class="btn btn-success">提交</button>
        </div>
    </form>


{% endblock content %}
```

urls

```
# 编辑跟进记录
url(r'^edit_follow_customer/(\d+)/', MyCustomer.AddEditFollowCustomerView.as_view(), name='edit_follow_customer'),
# 添加跟进记录
url(r'^add_follow_customer/', MyCustomer.AddEditFollowCustomerView.as_view(), name='add_follow_customer'),
```

## 编辑和添加报名记录

如上重复的操作，只需修改变量名和一些其他的小点即可。

## 编辑和添加课程记录

如上重复的操作，只需修改变量名和一些其他的小点即可。

## 公转私bug修改

当两个用户都进行转私户的操作时，之前的代码会出现最后一个转的人把客户都转到它的账户下。这是因为最后一个用户把cid提交后进行更新操作。我们借助事务来处理这个问题。

```python
# 事务
from django.db import transaction

    def reverse_gs(self, request, customer_ids):
        # 公转私bug修改
        with transaction.atomic():
            res_obj = models.CustomerInfo.objects.filter(pk__in=customer_ids, consultant_id__isnull=True).select_for_update()
            print(res_obj)
            if res_obj.count() != len(customer_ids):
                tag2 = 'gs_bug'
                tag1 = 'gs'
                return render(request, 'customer.html', {'customer_obj': res_obj,'tag1': tag1, 'tag2': tag2})
                # return HttpResponse('出错！')
        res_obj.update(consultant_id=request.session.get('user_id'))
```

customer.html里修改

```html
<h3>
    {% load my_tags %}
    {% if tag2 == 'gs_bug'%}
        由于你操作过慢，部分客户已经被其他用户转走，在你锁选择的客户中，目前可以转为你的私户的客户信息如下：
    {% else %}
    {% reverse_url request %}
    {% endif %}
</h3>
```
## modelformset批量生成和修改

```python
from django.forms.models import modelformset_factory



class StudyRecordModelForm(forms.ModelForm):

    class Meta:
        model = models.StudyRecord
        fields = '__all__'
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})

    
    
class StudyRecordView(View):

    def get(self, request):
        # study_record = models.StudyRecord.objects.filter(course_record_id=1).first()
        # print(study_record)
        # study_record_form = StudyRecordModelForm(instance=study_record)
        formset = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm)

        return render(request, 'study_records.html', {'formset': formset, })
    
    
  {% for study in formset %}

                <tr>
                <td>
        			# 就如csrf_token似的，提交修改必须加
                    {{ study.id }}

                    <input type="checkbox" value="" name="customer_ids"></td>
                    <td>{{ forloop.counter }}</td>
                    {#                <td>{{ customer.id }}</td>#}
                    <td>{{ study.instance.student}}</td>
                    <td>{{ study.course_record.class_grade}}</td>
                    <td>{{ study.score}}</td>
                    <td>{{ study.show_status}}</td>
                    <td>{{ study.note}}</td>
{#                    <td>{{ study.date}}</td>#}
{#                    <td><a href="{% url 'edit_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>#}
{#                    <td><a href="{% resolve_url request 'add_follow_customer' customer.id %}"><i class="fa fa-edit"></i></a></td>#}
{#                    <td><a href="{% resolve_url request 'edit_course_record' course_record.name.id %}"><i class="fa fa-edit"></i></a></td>#}
                </tr>

            {% endfor %}
```

## 用户权限分配

权限表结构RBAC，在权限菜单表中添加url和名，在role给角色配分不同权限，在UserInfo中给每个用户分配角色

```python
class UserInfo(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(to='Role')

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
```

用户登录成功后就把权限认证放进session中

```
# 登录
class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
        if user_obj:
            # return HttpResponse('ok')
            # 把当前用户id添加到session中
            request.session['user_id'] = user_obj.id
            # 把权限认证封装到session中
            permission = models.UserInfo.objects.filter(username=username).values('roles__menus__url_name').distinct()  # 身兼多职的话就去重一下
            permission_list = list(permission)
            request.session['permission_list'] = permission_list
            # print(permission_list)
            return redirect('home')
        else:
            # return redirect('login')
            return render(request, 'login.html', {'error': '用户名或密码错误！'})
```

在中间件中完成权限认证

```python
class MyLoginAuth(MiddlewareMixin):

    def process_request(self, request):

        user_id = request.session.get('user_id')
        permission = request.session.get('permission_list')
        path = request.path
        # print(path)
        # /lol/follow_customer/
        # 登录认证
        # 白名单
        white_list = [reverse('login'), reverse('register'), reverse('login_out')]
        if path in white_list:
            return

        if not user_id:
            return redirect('login')
        # 登录成功
        # 将当前登录用户对象封装到request类中，成为它的一个属性，这样就可以在后边的request中直接使用
        request.user_obj = models.UserInfo.objects.get(id=user_id)
        # 权限认证
        # 权限认证白名单
        permission_white_list = [reverse('home')]
        if path in permission_white_list:
            return
        for url in permission:
            res = re.match(url['roles__menus__url_name'], path)
            # print(res)
            # print(url['roles__menus__url_name'])
            if res:
                return
        else:
            return HttpResponse('您不配！')
```
## 根据用户权限动态生成菜单

把是菜单的路径写个标志登陆时一起存在session中

```python
permission = models.UserInfo.objects.filter(username=username).values('roles__menus__url_name', 'roles__menus__url_type', 'roles__menus__name').distinct()  # 身兼多职的话就
```

在菜单生成出引入自己的自定义inclusion

```html
<ul class="nav nav-treeview">

    {% load my_tags %}
    {% menu request %}

</ul>
```

my_tags

```python
@register.inclusion_tag('menu.html')
def menu(request):
    menu_list = []
    path = request.path
    permission = request.session.get('permission_list')
    for url in permission:
        if url['roles__menus__url_type']:
            menu_list.append(url)
        if path == url['roles__menus__url_name']:
            url['active'] = 'active'

    # print(menu_list)

    return {'menu_list': menu_list}
```

menu.html

```html
{% for menu in menu_list %}
    <li class="nav-item">
        <a href="{{ menu.roles__menus__url_name }}" class="nav-link {{menu.active}}">
            <i class="far fa-circle nav-icon"></i>
            <p>{{ menu.roles__menus__name }}</p>
        </a>
    </li>
{% endfor %}
```
## 动态二级菜单

设计注入到session中的数据结构，其中把一级菜单做个标记，然后找到它对应的二级菜单，并加入他所在的键值对的chirldren中。最后再session中获取，在渲染时，设置二级菜单标签css样式，绑定js点击事件，一点击就取消它的hiden类属性。

## 菜单排序

在菜单表中给每一个菜单加一个权重，然后再处理时按权重排完序后再循进行环模板渲染。

model中增加一个权重字段，然后给他们赋值不同的权重

```python
class Menus(models.Model):
    """动态菜单"""
    name = models.CharField('菜单名', max_length=32)

    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField('连接', max_length=128)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '菜单'
        unique_together = ('name', 'url_name')

    def __str__(self):
        return self.name
```

inclusion_tag中对之前处理的menu_list根据weight进行排序再取逆序使得最大权重排在第一位

```python
@register.inclusion_tag('menu.html')
def menu(request):
    menu_list = []
    path = request.path
    permission = request.session.get('permission_list')
    # print('permission:', permission)
    for url in permission:
        if url['roles__menus__url_type']:
            menu_list.append(url)
        if path == url['roles__menus__url_name']:
            url['active'] = 'active'

    # print('menu_list:', menu_list)
    # 根据weight排序
    menu_list = sorted(menu_list, key=lambda dic: dic['roles__menus__weight'], reverse=True)

    # print(menu_list)

    return {'menu_list': menu_list}
```

## 点击二级菜单的子菜单后二级菜单仍然处于选中状态

在menu表中添加一个parent_id字段，它自关联到主键，在登录时把他注入到session中：

```
parent_id = models.ForeignKey('self', null=True, blank=True)
```

在中间件中给request封装一个属性request.current_id = pid

```python
# 标签当前的id
request.current_id = None

if res:
    pid = url['roles__menus__parent_id']
    if pid:
        request.current_id = pid
    else:
        request.current_id = url['roles__menus__pk']
```

在自定义menu标签中，本来通过判断当前路径给菜单加active类，现在根据当前路径的pk值与封装到的current_id比较即可

```python
for url in permission:
    if url['roles__menus__url_type']:
        menu_list.append(url)
    # if path == url['roles__menus__url_name']:
    if request.current_id == url['roles__menus__pk']:
        url['active'] = 'active'
```

## 二级菜单路径导航和面包屑

```python
# 中间件中加面包屑

		# 面包屑路径导航
        request.bread_crumbs = [
            {'url': reverse('home'), 'title': '首页'},
        ]

        for url in permission:
            # pattern = '^' + url['roles__menus__url_name'] + '$'

            res = re.match(url['roles__menus__url_name'], path)
            # print(url['roles__menus__url_type'])
            # print(url['roles__menus__url_name'])
            if res:
                pid = url['roles__menus__parent_id']
                if pid:
                    request.current_id = pid
                    for data in permission:
                        # 三级菜单面包屑
                        if data['roles__menus__pk'] == pid:
                            # 有一层循环可能耗费事件，可以提前把注入session的数据处理一下，弄成字典
                            request.bread_crumbs.append(
                                {'url': data['roles__menus__url_name'], 'title': data['roles__menus__name']}
                            )
                            break
                    # 二级菜单面包屑
                    request.bread_crumbs.append(
                        {'url': None, 'title': url['roles__menus__name']}
                    )
                else:
                    request.current_id = url['roles__menus__pk']
                # print(url['roles__menus__parent_id'])
                    # 二级菜单面包屑
                    request.bread_crumbs.append(
                        {'url': None, 'title': url['roles__menus__name']}
                    )
                return
```

导航栏动态生成

```python
<ol class="breadcrumb m-lg-3">
    {#            <li><a href="{% url 'home' %}">主页</a></li>#}
    {% for bread in request.bread_crumbs %}
        {% if bread.url %}
            <li><a href="{{ bread.url }}">{{ bread.title }}</a></li>
        {% else %}
            <li class="active">{{ bread.title }}</li>
        {% endif %}
    {% endfor %}
</ol>
```

![image-20201203191502800](https://img-blog.csdnimg.cn/img_convert/eb2b93d9b5845cec4179a62418f95dc2.png)

## 权限精确到按钮级别

在model表中增加一个url别名字段，然后自定义一个过滤器判断别名在不在session中，最后动态渲染。

菜单表增加别名字段url_other_name

```python
class Menus(models.Model):
    """动态菜单"""
    name = models.CharField('菜单名', max_length=32)

    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic'),
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField('连接', max_length=128)
    url_other_name = models.CharField(max_length=128, null=True, blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = '菜单'
        unique_together = ('name', 'url_name')

    def __str__(self):
        return self.name
```

自定义过滤器处理别名

```python
@register.filter
def url_button(request, name):
    permission = request.session.get('permission_list')
    url_name = []
    for url in permission:
        if url['roles__menus__url_other_name']:
            url_name.append(url['roles__menus__url_other_name'])
    # print(url_name)
    if name in url_name:
        return True
    else:
        return False
```

在生成按钮的地方使用过滤器

```html
{% if request|url_button:'add_customer' %}
<h3><a href="{% url 'add_customer' %}">添加客户</a></h3>
{% endif %}
```





## 完整项目地址

我的码云：

[https://gitee.com/libo-sober/super-crm/](https://gitee.com/libo-sober/super-crm/)






