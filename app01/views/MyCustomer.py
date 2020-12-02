from django.shortcuts import (
    render, redirect, HttpResponse,
)
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.db import transaction
from django.forms.models import modelformset_factory

from app01 import models
from app01.utils.page_html import MyPagination
from modelform import settings
from app01.views.MyForms import (
    CustomerForm, FollowCustomerForm, EnrollmentForm, CourseRecordForm, StudyRecordModelForm,
)

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
            # 反射
            ret = getattr(self, gs_sg)(request, customer_ids)
            if ret:
                return ret
            return redirect(request.path)

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

    def reverse_sg(self, request, res_obj):
        res_obj.update(consultant_id=None)



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
        customer_form = CustomerForm(data=request.POST, instance=customer_obj)
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
        cid = request.GET.get('cid')  # 在customer里有个查看详情的href发来的get请求携带的关键字
        page_id = request.GET.get('page')  # 获取get请求中的page数据
        search_field = request.GET.get('search_field')  # 获取get请求中的搜索字段
        search = request.GET.get('search')  # 获取get请求中的搜索数据
        # print(search)
        # print(cid)
        if cid:
            cur_follow_customer = models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0, customer_id=cid).order_by('-date')
        else:
            cur_follow_customer = models.CustomerFollowUp.objects.filter(user=request.user_obj, delete_status=0).order_by('-date')
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
        obj = models.CustomerFollowUp.objects.filter(customer_id__in=customer_ids)
        # 假删
        obj.update(delete_status=1)

        return redirect(request.path)


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
        follow_customer_form = FollowCustomerForm(request, request.POST, instance=follow_customer_obj)
        next_url = request.GET.get('next')
        # print(next_url)
        if follow_customer_form.is_valid():
            follow_customer_form.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('follow_customer')
        else:
            return render(request, 'add_follow_customer.html', {'follow_customer_form': follow_customer_form, 'label':label})


# 报名记录
class EnrollmentView(View):

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
            student_obj = models.StudentEnrollment.objects.filter(consultant=request.user_obj, customer_id=cid)
        else:
            student_obj = models.StudentEnrollment.objects.filter(consultant=request.user_obj,)
        if search:
            q_obj = Q()
            q_obj.children.append((search_field, search))
            customer_obj_list = student_obj.filter(q_obj)
        else:
            customer_obj_list = student_obj.all()
        print(customer_obj_list)
        num = customer_obj_list.count()  # 总共记录数
        # print(num)
        base_url = request.path  # 请求路径
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        enrollment = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        return render(request, 'student_enrollment.html', {'enrollment': enrollment, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name,})


# 添加和编辑报名记录
class AddEditEnrollmentView(View):

    def get(self, request, cid=None):
        label = '编辑报名信息' if cid else '添加报名信息'
        student_obj= models.StudentEnrollment.objects.filter(consultant=request.user_obj, customer_id=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
        # print(student_obj, cid)
        enrollment_form = EnrollmentForm(request, instance=student_obj)
        return render(request, 'add_enrollment.html', {'enrollment_form':enrollment_form, 'label':label})

    def post(self, request, cid=None):
        label = '编辑跟进客户' if cid else '添加跟进客户'
        student_obj = models.StudentEnrollment.objects.filter(consultant=request.user_obj, customer_id=cid).first()
        enrollment_form = EnrollmentForm(request, data=request.POST, instance=student_obj)
        next_url = request.GET.get('next')
        print(next_url)
        if enrollment_form.is_valid():
            enrollment_form.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('student_enrollment')
        else:
            return render(request, 'add_enrollment.html', {'enrollment_form': enrollment_form, 'label':label})


# 上课记录
class CourseRecordView(View):

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
            course_records_obj = models.CourseRecord.objects.filter(teacher=request.user_obj, name_id=cid)
        else:
            course_records_obj = models.CourseRecord.objects.filter(teacher=request.user_obj,)
        if search:
            q_obj = Q()
            q_obj.children.append((search_field, search))
            customer_obj_list = course_records_obj.filter(q_obj)
        else:
            customer_obj_list = course_records_obj.all()
        # print(customer_obj_list)
        num = customer_obj_list.count()  # 总共记录数
        # print(num)
        base_url = request.path  # 请求路径
        page_count = settings.PAGE_COUNT  # 页数栏显示多少个数
        record = settings.RECORD  # 每页显示多少条记录

        html_obj = MyPagination(page_id=page_id, num=num, base_url=base_url, get_data=get_data, page_count=page_count, record=record)

        course_records = customer_obj_list[(html_obj.page_id - 1) * html_obj.record:html_obj.page_id * html_obj.record]
        return render(request, 'course_records.html', {'course_records': course_records, 'page_html': html_obj.html_page(), 'cur_user_name': cur_user_name,})

    def post(self, request):

        print(request.POST)
        customer_ids = request.POST.getlist('customer_ids')
        student_obj = models.Student.objects.filter(customer_id__in=customer_ids)
        study_record_obj = []
        for student in student_obj:
            study = models.StudyRecord(
                student=student,
                course_record=models.CourseRecord.objects.get(name_id=student.customer_id),
            )
            study_record_obj.append(study)
        models.StudyRecord.objects.bulk_create(study_record_obj)

        return redirect(request.path)

# 编辑和添加上课记录
class AddEditCourseRecordView(View):

    def get(self, request, cid=None):
        label = '编辑课程信息' if cid else '添加课程信息'
        course_records_obj = models.CourseRecord.objects.filter(teacher=request.user_obj, name_id=cid).first()  # filter返回的时一个QuerrySet集合，取出里边的model对象
        # print(student_obj, cid)
        course_record_form = CourseRecordForm(request, instance=course_records_obj)
        return render(request, 'add_course_record.html', {'course_record_form':course_record_form, 'label':label})

    def post(self, request, cid=None):
        label = '编辑课程信息' if cid else '添加课程信息'
        course_records_obj = models.CourseRecord.objects.filter(teacher=request.user_obj, name_id=cid).first()
        course_record_form = CourseRecordForm(request, data=request.POST, instance=course_records_obj)
        next_url = request.GET.get('next')
        # print(next_url)
        if course_record_form.is_valid():
            course_record_form.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('course_records')
        else:
            return render(request, 'add_course_record.html', {'course_record_form': course_record_form, 'label':label})



class StudyRecordView(View):

    def get(self, request):
        # study_record = models.StudyRecord.objects.filter(course_record_id=1).first()
        # print(study_record)
        # study_record_form = StudyRecordModelForm(instance=study_record)
        formset = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm)

        return render(request, 'study_records.html', {'formset': formset, })
