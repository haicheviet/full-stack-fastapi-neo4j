from celery import Celery

from app.core import celary_config
from app.core.config import settings


def make_celery():
    celery = Celery("worker",
                    backend=settings.CELERY_RESULT_BACKEND,
                    broker=settings.CELERY_BROKER)
    celery.conf.update(settings)
    celery.config_from_object(celary_config)

    return celery


celery_app = make_celery()
