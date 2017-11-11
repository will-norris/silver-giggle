import logging
from random import choices
import string

from celery import task
from celery.signals import task_success
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@task(bind=True)
def log(self):
    message = ''.join(choices(string.ascii_uppercase + string.digits, k=30))
    logger.warning('Sending {} for silver_giggle.consumer.tasks.log'.format(message))
    self.app.send_task('silver_giggle.consumer.tasks.log', args=(message,))


@task_success.connect
def task_success_handler(sender=None, headers=None, body=None, **kwargs):
    logger.error('Successful {} task'.format(sender))
