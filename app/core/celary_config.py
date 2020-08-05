from celery.schedules import crontab

CELERY_IMPORTS = 'app.core.task.periodic_task'
CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'schedule_back_up_every_day': {
        'task': 'app.core.task.periodic_task.back_up_scrip',
        'schedule': crontab(minute=0, hour=0)  # Execute daily at midnight
    }
}
