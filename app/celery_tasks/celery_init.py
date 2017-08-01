from celery import Celery
from celery.utils.log import get_task_logger

from app import celery_settings

celery = Celery("celery_tasks", backend=celery_settings.CELERY_RESULT_BACKEND, broker=celery_settings.BROKER_URL)
logger = get_task_logger(__name__)

celery.config_from_object(celery_settings)
