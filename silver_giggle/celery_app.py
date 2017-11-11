from datetime import timedelta
from os import environ
from random import randint
import logging
from uuid import uuid4

from celery import Celery, task
from kombu import Exchange, Queue, binding, Connection

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


# task to be used by both producers and consumers - producer publishes the task to queues, consumers execute
@task(name='pub_sub_task')
def log(message):
    logger.info('Received {}'.format(message))


def init_celery(name, queue_name=None):
    """
    Initializing celery to point to a rabbitmq type of broker
    """
    app = Celery(
        'silver_giggle.{}'.format(name),
        broker=environ['BROKER_CNX_STRING']
    )

    # only create queues and bindings for consumers
    if queue_name:
        message_exchange = Exchange('message_exchange')

        app.conf.task_queues = (
            Queue(queue_name, [
                # bind queue to exchange using routing key content_groups
                binding(message_exchange, 'content_groups')
            ]),
        )

    # register the task on each app
    app.register_task(log)

    return app


def init_producer():
    app = init_celery('producer')

    # have to supply an exchange object to celerybeat - only giving the name of the exchange doesnt work
    message_exchange = Exchange('message_exchange')

    app.conf.beat_schedule = {
        'log': {
            'task': 'pub_sub_task',
            'schedule': timedelta(seconds=5),
            'args': (str(uuid4()),),
            'options': {'routing_key': 'content_groups', 'exchange': message_exchange}
        },
    }

    return app


def init_consumer():
    app = init_celery('consumer#{}'.format(randint(1, 1000)), 'consumer_queue')

    return app


def init_consumer2():
    app = init_celery('consumer#{}'.format(randint(1, 1000)), 'consumer2_queue')

    return app
