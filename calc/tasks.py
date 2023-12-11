# tasks.py

from celery import Celery
from .models import SurftStatus

app = Celery('calc')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def run_surft_results(query, num_results):
    try:
        # Call your SurftResults function here
        SurftResults(query, num_results)
    finally:
        # Mark the status as not running when finished
        SurftStatus.objects.update(is_running=False)