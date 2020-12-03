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
        # 面包屑路径导航
        request.bread_crumbs = [
            {'url': reverse('home'), 'title': '首页'},
        ]
        # 标签当前的id
        request.current_id = None
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
        # print(permission)
        for url in permission:
            # pattern = '^' + url['roles__menus__url_name'] + '$'

            res = re.match(url['roles__menus__url_name'], path)
            # print(url['roles__menus__url_type'])
            # print(url['roles__menus__url_name'])
            if res:
                pid = url['roles__menus__parent_id']
                if pid:
                    request.current_id = pid
                    for data in permission:
                        # 三级菜单面包屑
                        if data['roles__menus__pk'] == pid:
                            # 有一层循环可能耗费事件，可以提前把注入session的数据处理一下，弄成字典
                            request.bread_crumbs.append(
                                {'url': data['roles__menus__url_name'], 'title': data['roles__menus__name']}
                            )
                            break
                    # 二级菜单面包屑
                    request.bread_crumbs.append(
                        {'url': None, 'title': url['roles__menus__name']}
                    )
                else:
                    request.current_id = url['roles__menus__pk']
                # print(url['roles__menus__parent_id'])
                    # 二级菜单面包屑
                    request.bread_crumbs.append(
                        {'url': None, 'title': url['roles__menus__name']}
                    )
                return
        else:
            return HttpResponse('您不配！')







