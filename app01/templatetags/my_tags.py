from django.urls import reverse
from django import template
from django.http.request import QueryDict
register = template.Library()


@register.simple_tag
def reverse_url(request):

    if request.path == reverse('customer'):
        return '公户信息'
    else:
        return '我的客户信息'


@register.simple_tag
def resolve_url(request, url_name, pk):
    next_url = request.get_full_path()
    # print(next_url)  # /customer/
    destination = reverse(url_name, args=(pk,))
    qd =QueryDict(mutable=True)  # mutable 可不可变，默认是False
    qd['next'] = next_url
    full_url = destination + '?' + qd.urlencode()  # /edit_customer/723/?next=%2Fcustomer%2F%3Fpage%3D2 按照ascii码十六进制替换/ ？ &
    # / customer /?search_field = contact__contains & search = 8 & page = 4
    # /edit_customer/703/?next=%2Fcustomer%2F%3Fsearch_field%3Dcontact__contains%26search%3D8%26page%3D4
    # 不用urlencode会导致在带有搜索条件的查询时，在后端request.get不到完整的？后变的信息
    # full_url = destination + '?next=' + next_url  # /edit_customer/714/?next=/customer/?page=2
    # print(full_url)
    return full_url


@register.inclusion_tag('menu.html')
def menu(request):
    menu_list = []
    path = request.path
    permission = request.session.get('permission_list')
    # print('permission:', permission)
    # print(request.current_id)
    for url in permission:
        if url['roles__menus__url_type']:
            menu_list.append(url)
        # if path == url['roles__menus__url_name']:
        # 现在判断，你访问这个url的父级菜单如果和你当前记录的pid一样，让他处于选中状态
        # 当前记录的pid就是 如果你是一个二级菜单，pid就是你的pk，如果你是个二级菜单下的一个子菜单，就记录你这个子菜单的parent_id,也就是它对应父级菜单的pk
        if request.current_id == url['roles__menus__pk']:
            url['active'] = 'active'

    # print('menu_list:', menu_list)
    # 根据weight排序
    menu_list = sorted(menu_list, key=lambda dic: dic['roles__menus__weight'], reverse=True)

    # print(menu_list)

    return {'menu_list': menu_list}


@register.filter
def url_button(request, name):
    permission = request.session.get('permission_list')
    url_name = []
    for url in permission:
        if url['roles__menus__url_other_name']:
            url_name.append(url['roles__menus__url_other_name'])
    # print(url_name)
    if name in url_name:
        return True
    else:
        return False
