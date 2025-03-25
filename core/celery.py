import os
from celery import Celery

# Ensure Django settings module is set for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('users')

# Load task modules from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
