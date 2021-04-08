import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tv_project.settings')
from django.core.mail import send_mail
app = Celery('tv_project')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

