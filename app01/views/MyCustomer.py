from django.shortcuts import (
    render, redirect
)
from django.urls import reverse
from django.views import View
from django import forms
from django.db.models import Q

from app01 import models
from app01.utils.page_html import MyPagination
from modelform import settings

# Create your views here.


# 主页
class HomeView(View):

    def get(self, request):

        user_id = request.session.get('user_id')
        cur_user_name = models.UserInfo.objects.get(id=user_id)
        return render(request, 'home.html', {'cur_user_name': cur_user_name})


# 客户处理
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
            tag1 = 'sg'
            cur_user_customer = models.CustomerInfo.objects.filter(consultant_id=user_id)
        else:
            tag1 = 'gs'
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
        return render(request, 'customer.html', {'customer_obj': customer_obj, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name, 'tag1':tag1})

    def post(self, request):
        # print(request.POST, request.path)
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


# 客户表单验证
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


# 编辑和添加客户信息
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
        next_url = request.GET.get('next')
        print(next_url)
        if customer_form.is_valid():
            customer_form.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('customer')
        else:
            return render(request, 'add_customer.html', {'customer_form': customer_form, 'label':label})


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

# 跟进客户modelform
class FollowCustomerForm(forms.ModelForm):

    class Meta:
        model = models.CustomerFollowUp
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


# 添加和编辑跟进客户信息
class AddEditFollowCustomerView(View):

    def get(self, request, cid=None):
        label = '编辑跟进客户' if cid else '添加跟进客户'
        follow_customer_obj= models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0, customer_id=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
        # print(follow_customer_obj, cid)
        follow_customer_form = FollowCustomerForm(instance=follow_customer_obj)
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