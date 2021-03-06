from django.contrib import admin
from app01 import models
# Register your models here.
# 自定义显示格式
# Admin高级定制


# class UserInfoAdmin(admin.ModelAdmin):
#     list_display = ['username', 'password', 'email', 'is_active', 'telephone'] # 展示
#     list_editable = ['password', 'email', 'telephone', ] # 直接修改
class MenusAdmin(admin.ModelAdmin):
    list_display = ['name', 'url_type', 'url_name', 'url_other_name', 'weight', 'parent_id']
    list_editable = ['url_type', 'url_name', 'url_other_name', 'weight', 'parent_id']

admin.site.register(models.UserInfo)
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.CustomerInfo)
admin.site.register(models.Menus, MenusAdmin)
admin.site.register(models.Role)
admin.site.register(models.StudyRecord)
admin.site.register(models.StudentEnrollment)



