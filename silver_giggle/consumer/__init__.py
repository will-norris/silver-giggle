from os import environ

from kombu import Exchange, Queue, binding

from silver_giggle.celery import init_celery


def init_consumer():
    app = init_celery('consumer.{}'.format(environ['CELERY_NAME']), 'silver_giggle.consumer')

    broadcasting_exchange = Exchange('silver_giggle.producer.broadcast')

    # give queue for service-a multiple bindings
    if environ['CELERY_NAME'] == 'service-a':
        app.conf.task_queues = (
            Queue(environ['CELERY_NAME'], [
                binding(broadcasting_exchange, routing_key='complex_groups'),
                binding(broadcasting_exchange, routing_key='kdm_groups')
            ]),
        )
    else:
        app.conf.task_queues = (
            Queue(environ['CELERY_NAME'], [
                binding(broadcasting_exchange, routing_key='complex_groups'),
            ]),
        )

    return app


# consumer celery app
app = init_consumer()
