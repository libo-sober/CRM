"""modelform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from app01.views import (
    MyAuth, MyCustomer
)

urlpatterns = [

    # 登录
    url(r'^login/', MyAuth.LoginView.as_view(), name='login'),
    # 登出
    url(r'^login_out/', MyAuth.LoginOutView.as_view(), name='login_out'),
    # 注册
    url(r'^register/', MyAuth.RegisterView.as_view(), name='register'),
    # 主页
    url(r'^home/', MyCustomer.HomeView.as_view(), name='home'),
    # 公共客户信息
    url(r'^customer/', MyCustomer.CustomerView.as_view(), name='customer'),
    # 我的客户信息
    url(r'^my_customer/', MyCustomer.CustomerView.as_view(), name='my_customer'),
    # 增加客户信息
    url(r'^add_customer/', MyCustomer.AddEditCustomer.as_view(), name='add_customer'),
    # 编辑客户信息
    url(r'^edit_customer/(\d+)/', MyCustomer.AddEditCustomer.as_view(), name='edit_customer'),
    # 跟进记录
    url(r'^follow_customer/', MyCustomer.FollowCustomerView.as_view(), name='follow_customer'),
    # 编辑跟进记录
    url(r'^edit_follow_customer/(\d+)/', MyCustomer.AddEditFollowCustomerView.as_view(), name='edit_follow_customer'),
    # 添加跟进记录
    url(r'^add_follow_customer/', MyCustomer.AddEditFollowCustomerView.as_view(), name='add_follow_customer'),
    # 添加报名记录
    url(r'^add_enrollment/', MyCustomer.AddEditEnrollmentView.as_view(), name='add_enrollment'),
    # 编辑报名记录
    url(r'^edit_enrollment/(\d+)/', MyCustomer.AddEditEnrollmentView.as_view(), name='edit_enrollment'),
    # 报名记录
    url(r'^student_enrollment/', MyCustomer.EnrollmentView.as_view(), name='student_enrollment'),
    # 上课记录
    url(r'^course_records/', MyCustomer.CourseRecordView.as_view(), name='course_records'),
    # 编辑上课记录
    url(r'^edit_course_record/(\d+)/', MyCustomer.AddEditCourseRecordView.as_view(), name='edit_course_record'),
    # 添加上课记录
    url(r'^add_course_record/', MyCustomer.AddEditCourseRecordView.as_view(), name='add_course_record'),
    # 学习记录
    url(r'^study_record/', MyCustomer.StudyRecordView.as_view(), name='study_record'),
    # 权限展示
    url(r'^role/list/', MyCustomer.RoleView.as_view(), name='role_list'),
]
