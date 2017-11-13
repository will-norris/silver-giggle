from datetime import timedelta

from kombu import Exchange, Queue, binding

from silver_giggle.celery import init_celery


def init_producer():
    app = init_celery('producer', 'silver_giggle.producer')

    broadcast_exchange = Exchange('silver_giggle.producer.broadcast')

    app.conf.task_queues = (
        Queue('silver_giggle.producer.broadcast', broadcast_exchange),
        Queue('silver_giggle.producer', Exchange('silver_giggle.producer')),
    )

    app.conf.task_routes = {
        'silver_giggle.producer.tasks.log': 'silver_giggle.producer',
        'silver_giggle.consumer.tasks.log': {
            'exchange': 'silver_giggle.producer.broadcast',
            # change the routing key here to kdm groups and then restart the services - you will see that
            # only service-a receives the message as it was the only one created with the kdm_groups binding
            # scaling up works too, the message in only received by one service-a worker
            'routing_key': 'kdm_groups'
        },
    }

    app.conf.beat_schedule = {
        'log': {
            'task': 'silver_giggle.producer.tasks.log',
            'schedule': timedelta(seconds=1),
            'args': (30,),
        },
        'fake_log': {
            'task': 'silver_giggle.producer.tasks.fake_log',
            'schedule': timedelta(seconds=1),
            'args': (10,),
        }
    }

    return app


# producer celery app
app = init_producer()
