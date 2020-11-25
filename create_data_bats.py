import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modelform.settings")
    import django
    django.setup()
    from app01 import models

    obj_list = []
    for i in range(200):
        d= {
            # 'name':
        }