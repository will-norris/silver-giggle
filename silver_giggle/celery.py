from datetime import timedelta
from os import environ
from random import randint

from celery import Celery
from kombu import Exchange, Queue, binding


def init_celery(name, tasks_pkg):
    """
    Initializing celery to point to a rabbitmq type of broker
    """
    app = Celery(
        'silver_giggle.{}'.format(name),
        broker=environ['BROKER_CNX_STRING']
    )

    app.autodiscover_tasks([tasks_pkg], force=True)

    return app


def init_producer():
    app = init_celery('producer', 'silver_giggle.producer')

    message_exchange = Exchange('message_exchange')

    app.conf.beat_schedule = {
        'log': {
            'task': 'silver_giggle.producer.tasks.log',
            'schedule': timedelta(seconds=5),
            'args': (),
            'options': {'routing_key': 'content_groups', 'exchange': 'message_exchange'}
        },
    }

    return app


def init_consumer(producer_name):
    app = init_celery('consumer#{}'.format(randint(1, 1000)), 'silver_giggle.consumer')

    message_exchange = Exchange('message_exchange')

    app.conf.task_queues = (
        Queue('consumer_queue', [
            binding(message_exchange, 'content_groups')
        ]),
    )

    return app
