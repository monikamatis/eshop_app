import os
from celery import Celery


# set up the default Django settings module for the 'celery' program

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_shop_app.settings')
app = Celery('E_shop_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
