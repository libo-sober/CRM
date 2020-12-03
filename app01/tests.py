from django.test import TestCase

# Create your tests here.
menu_list = [
    {'roles__menus__url_name': '/lol/follow_customer/', 'roles__menus__url_type': 1, 'roles__menus__name': '跟进记录',
     'roles__menus__weight': 80},
    {'roles__menus__url_name': '/lol/my_customer/', 'roles__menus__url_type': 1, 'roles__menus__name': '我的客户',
     'roles__menus__weight': 90},
    {'roles__menus__url_name': '/lol/customer/', 'roles__menus__url_type': 1, 'roles__menus__name': '公共客户',
     'roles__menus__weight': 100},
    {'roles__menus__url_name': '/lol/student_enrollment/', 'roles__menus__url_type': 1, 'roles__menus__name': '报名记录',
     'roles__menus__weight': 70},
    {'roles__menus__url_name': '/lol/course_records/', 'roles__menus__url_type': 1, 'roles__menus__name': '上课记录',
     'roles__menus__weight': 60},
    {'roles__menus__url_name': '/lol/study_record/', 'roles__menus__url_type': 1, 'roles__menus__name': '学习记录',
     'roles__menus__weight': 50}
]

menu_list = sorted(menu_list, key=lambda dic:dic['roles__menus__weight'], reverse=True)

print(menu_list)

