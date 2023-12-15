from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Surfter.settings')

app = Celery('Surfter')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# app.conf.update(
#     broker_url='amqp://guest:guest@localhost:5672//',
#     # other configuration settings...
#     worker_prefetch_multiplier=1,
# )