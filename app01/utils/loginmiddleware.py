import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from app01 import models


class MyLoginAuth(MiddlewareMixin):

    def process_request(self, request):
        # 白名单
        # print(request.path)
        # print(re.match(r'^/admin/', request.path).group())
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

