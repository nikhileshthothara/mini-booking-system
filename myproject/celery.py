import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "myproject.settings")
app = Celery('myproject')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_create_missing_queues = True
app.conf.timezone = 'UTC'