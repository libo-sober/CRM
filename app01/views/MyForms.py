import re

from django.core.exceptions import ValidationError
from django import forms

from app01 import models


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
                print(type(field), field_name)
                field.widget.attrs.update({'type': 'date'})
            field.widget.attrs.update({'class': 'form-control'})


# 跟进客户modelform
class FollowCustomerForm(forms.ModelForm):

    class Meta:
        model = models.CustomerFollowUp
        fields = '__all__'
        exclude = ['delete_status', ]
        error_messages = {
            'customer': {'required': '不能为空！'},
            'content': {'required': '不能为空！'},
            'user': {'required': '不能为空！'},
            'status': {'required': '不能为空！'},
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # modelform默认会生成这个外键关联的表的所有信息，就是models.CustomerInfo.objects.all()
            # 我们只想显示当前用户下的客户信息
            if field_name == 'customer':
                field.queryset = models.CustomerInfo.objects.filter(consultant=request.user_obj)
            elif field_name == 'user':
                # field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.id)
                field.choices = ((request.user_obj.id, request.user_obj.username),)


# 报名信息
class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = models.StudentEnrollment
        fields = '__all__'
        # exclude = ['delete_status', ]
        error_messages = {
            'why_us': {'required': '不能为空！'},
            'target': {'required': '不能为空！'},
            'customer': {'required': '不能为空！'},
            'class_grade': {'required': '不能为空！'},
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # modelform默认会生成这个外键关联的表的所有信息，就是models.CustomerInfo.objects.all()
            # 我们只想显示当前用户下的客户信息
            if field_name == 'customer':
                field.queryset = models.CustomerInfo.objects.filter(consultant=request.user_obj)
            elif field_name == 'consultant':
                # field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.id)
                field.choices = ((request.user_obj.id, request.user_obj.username),)
            from django.forms.fields import DateTimeField
            # 如果是日期，换成类型位日期类型的输入框

            if isinstance(field, DateTimeField):
                print(type(field))
                field.widget.attrs.update({'type': 'date'})


class CourseRecordForm(forms.ModelForm):

    class Meta:
        model = models.CourseRecord
        fields = '__all__'
        # exclude = ['delete_status', ]
        # error_messages = {
        #     'why_us': {'required': '不能为空！'},
        #     'target': {'required': '不能为空！'},
        #     'customer': {'required': '不能为空！'},
        #     'class_grade': {'required': '不能为空！'},
        # }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # modelform默认会生成这个外键关联的表的所有信息，就是models.CustomerInfo.objects.all()
            # 我们只想显示当前用户下的客户信息
            if field_name == 'name':
                field.queryset = models.CustomerInfo.objects.filter(consultant=request.user_obj)
            elif field_name == 'teacher':
                # field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.id)
                field.choices = ((request.user_obj.id, request.user_obj.username),)
            from django.forms.fields import DateTimeField
            # 如果是日期，换成类型位日期类型的输入框

            if isinstance(field, DateTimeField):
                print(type(field))
                field.widget.attrs.update({'type': 'date'})


class StudyRecordModelForm(forms.ModelForm):

    class Meta:
        model = models.StudyRecord
        fields = '__all__'
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})

