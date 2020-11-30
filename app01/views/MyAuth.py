from django.shortcuts import (
    render, redirect
)
from django.views import View

from app01 import models
from app01.utils.hashlib_func import set_md5
from app01.views.MyForms import (
    RegisterForm,
)

# Create your views here.


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
