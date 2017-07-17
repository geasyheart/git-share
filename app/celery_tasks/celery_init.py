from celery import Celery
from celery.utils.log import get_task_logger

from app import celery_settings

celery = Celery("celery_tasks", backend='rpc', broker='amqp://zy:123456@172.17.0.1:5672//')
logger = get_task_logger(__name__)

celery.config_from_object(celery_settings)
