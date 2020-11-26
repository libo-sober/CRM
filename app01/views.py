import re

from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views import View
from django import forms
from django.db.models import Q

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
            # 把当前用户id添加到session中
            request.session['user_id'] = user_obj.id
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

        user_id = request.session.get('user_id')
        cur_user_name = models.UserInfo.objects.get(id=user_id)
        return render(request, 'home.html', {'cur_user_name': cur_user_name})


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
            tag = 'sg'
            cur_user_customer = models.CustomerInfo.objects.filter(consultant_id=user_id)
        else:
            tag = 'gs'
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
        # print(num)
        base_url = request.path  # 请求路径
        # 以后直接在settings配置文件中修改即可
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录
        # print(base_url)

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        customer_obj = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        # print(page_id)
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name, 'tag':tag})

    def post(self, request):
        print(request.POST)
        gs_sg = request.POST.get('gs_sg')
        customer_ids = request.POST.getlist('customer_ids')
        if hasattr(self, gs_sg):
            res_obj = models.CustomerInfo.objects.filter(pk__in=customer_ids)
            getattr(self, gs_sg)(request, res_obj)
            return redirect(request.path)


    def reverse_gs(self, request, res_obj):
        res_obj.update(consultant_id=request.session.get('user_id'))

    def reverse_sg(self, request, res_obj):
        res_obj.update(consultant_id=None)


class CustomerForm(forms.ModelForm):

    class Meta:
        model = models.CustomerInfo
        fields = '__all__'
        error_messages = {
            'name': {'required': '不能为空！'},
            'contact_type': {'required': '不能为空！'},
            'contact': {'required': '不能为空！'},
            'source': {'required': '不能为空！'},
            'consult_content': {'required': '不能为空！'},
            'status': {'required': '不能为空！'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            from django.forms.fields import DateField
            # 如果是日期，换成类型位日期类型的输入框
            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})
            field.widget.attrs.update({'class': 'form-control'})


# class AddCustomerView(View):
#
#     def get(self, request):
#         customer_form = CustomerForm()
#         return render(request, 'add_customer.html', {'customer_form': customer_form})
#
#     def post(self, request):
#         customer_form = CustomerForm(request.POST)
#         if customer_form.is_valid():
#             customer_form.save()
#             return redirect('customer')
#         else:
#             return render(request, 'add_customer.html', {'customer_form': customer_form})
#
#
# class EditCustomerView(View):
#
#     def get(self, request, cid):
#         customer_obj = models.CustomerInfo.objects.filter(pk=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
#         customer_form = CustomerForm(instance=customer_obj)
#         return render(request, 'edit_customer.html', {'customer_form':customer_form})
#
#     def post(self, request, cid):
#         customer_obj = models.CustomerInfo.objects.filter(pk=cid).first()
#         customer_form = CustomerForm(request.POST, instance=customer_obj)
#         if customer_form.is_valid():
#             customer_form.save()
#             return redirect('customer')
#         else:
#             return render(request, 'edit_customer.html', {'customer_form': customer_form})


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
