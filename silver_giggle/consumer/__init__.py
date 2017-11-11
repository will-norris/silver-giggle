from os import environ

from kombu import Exchange, Queue

from silver_giggle.celery import init_celery


def init_consumer():
    app = init_celery('consumer.{}'.format(environ['CELERY_NAME']), 'silver_giggle.consumer')

    # one per service
    exchange_name = 'silver_giggle.consumer.{}'.format(environ['CELERY_NAME'])
    service_exchange = Exchange(exchange_name, type='direct', channel=app.broker_connection().channel())
    service_exchange.declare()
    service_exchange.bind_to('silver_giggle.producer.broadcast')

    app.conf.task_queues = [
        Queue(app.main, Exchange(exchange_name, type='direct')),
    ]

    return app


# consumer celery app
app = init_consumer()
