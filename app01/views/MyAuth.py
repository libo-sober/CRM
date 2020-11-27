import re

from django.shortcuts import (
    render, redirect
)
from django.core.exceptions import ValidationError
from django.views import View
from django import forms

from app01 import models
from app01.utils.hashlib_func import set_md5

# Create your views here.


# 自定义验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  # 自定义验证规则的时候，如果不符合你的规则，需要自己发起错误


# 注册验证
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
            return redirect('home')
        else:
            # return redirect('login')
            return render(request, 'login.html', {'error': '用户名或密码错误！'})


# 登出
class LoginOutView(View):

    def get(self, request):
        request.session.flush()  # 清楚所有的cookie和session
        return redirect('login')


# 注册
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
