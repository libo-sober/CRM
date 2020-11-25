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
            names.append(line.strip())
    print(len(names))
    customer_obj = []
    for i in range(100, 180):

        obj = models.CustomerInfo(
            name=names[i-100],
            contact_type=random.randint(0, 2),
            contact=f'21321378{i}',
            source=random.randint(0, 5),
            referral_from_id=models.CustomerInfo.objects.get(id=1).id,
            consult_courses_id=models.Course.objects.get(id=1).id,
            consult_content='什么是'+names[i-100]+'?',
            status=random.randint(0, 2),
            consultant_id=models.UserInfo.objects.get(id=1).id
        )
        customer_obj.append(obj)
    models.CustomerInfo.objects.bulk_create(customer_obj)


