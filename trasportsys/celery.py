import os

from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trasportsys.settings')

app = Celery('trasportsys')

app.conf.beat_schedule = {
    'every_1_seconds': {
        'task': 'administration.tasks.calculate_daily_sales',
        'schedule': 1,

    },
    'every_day_1.00_A.M': {
        'task': 'administration.tasks.copy_n_del_ticket_to_the_recovery__db',
        'schedule': 3000,  # execute every 30 minutes

    },
    'every_day_1.10_A.M': {
        'task': 'administration.tasks.delete_records_more_then_3_days',
        'schedule': 3300,  # execute every 30 minutes

    },
    'every_day_1.15_A.M': {
        'task': 'administration.tasks.reschedule_routes_and_clean_up_db',
        'schedule': 3600,  # execute every 30 minutes

    },
    # 'test': {
    #     'task': 'administration.tasks.print2',
    #     'schedule': crontab(hour='1'),  # execute every 30 minutes
    #
    # }
}
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
