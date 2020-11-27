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

