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
from modelform import settings

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


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


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
