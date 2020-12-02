import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
from django.urls import reverse
from app01 import models


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







