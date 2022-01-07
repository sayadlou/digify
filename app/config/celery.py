import os 
from celery import Celery

os.environ.get('DJANGO_SETTINGS_MODULE')

celery = Celery('digify')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()