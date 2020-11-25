import os
import random

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modelform.settings")
    import django
    django.setup()
    from app01 import models
    names = []
    with open('statics/plugins/lol_name', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line != []:
                names.append(line)
    print(len(names))
    courses = models.Course.objects.all()
    r_name = models.UserInfo.objects.all()
    cus = models.CustomerInfo.objects.all()
    print(courses[0].id)
    print(r_name[0].id)
    print(cus[0].id)
    customer_obj = []
    models.CustomerInfo.objects.create(
        name='taitai',
    )
    # for i in range(100):
    #     d = {
    #         # 'id':i+3,
    #         'name':names[i+1],
    #         'contact_type':random.randint(0, 2),
    #         'source':random.randint(0, 5),
    #         # 'referral_from':cus[0],
    #         # 'consult_courses':courses[random.randint(0,3)].id,
    #         'consult_content':'什么是'+names[i+1]+'?',
    #         'status':random.randint(0, 2),
    #         # 'consultant':r_name[0],
    #     }
    #     obj = models.CustomerInfo(**d)
    #     customer_obj.append(obj)
    # models.CustomerInfo.objects.bulk_create(customer_obj)


