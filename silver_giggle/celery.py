from os import environ

from celery import Celery


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
