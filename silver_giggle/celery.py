from datetime import timedelta
from os import environ
from random import randint

from celery import Celery
from kombu import Exchange, Queue


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

    app.conf.task_queues = (
        Queue('silver_giggle.producer.broadcast', Exchange('silver_giggle.producer.broadcast', type='fanout')),
        Queue('silver_giggle.producer', Exchange('silver_giggle.producer')),
    )

    app.conf.task_routes = {
        'silver_giggle.producer.tasks.log': 'silver_giggle.producer',
        'silver_giggle.consumer.tasks.log': 'silver_giggle.producer.broadcast',
    }

    app.conf.beat_schedule = {
        'log': {
            'task': 'silver_giggle.producer.tasks.log',
            'schedule': timedelta(seconds=5),
            'args': (),
        },
    }

    return app


def init_consumer(producer_name):
    app = init_celery('consumer#{}'.format(randint(1, 1000)), 'silver_giggle.consumer')

    app.conf.task_create_missing_queues = False

    app.conf.task_queues = [
        Queue(app.main, Exchange('silver_giggle.producer.broadcast', type='fanout')),
    ]

    return app
