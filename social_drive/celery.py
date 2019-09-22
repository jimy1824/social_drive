import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_drive.settings')

app = Celery('social_drive', broker='redis://localhost:6379')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'auto_syscronization': {
        'task': 'drives_data.tasks.data_syscronization',
        'schedule': 86400.0,
    }
}
