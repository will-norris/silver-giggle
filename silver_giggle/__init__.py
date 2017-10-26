from silver_giggle.celery import init_producer, init_consumer


# producer celery app
producer = init_producer()

# consumer celery app
consumer = init_consumer(producer.main)
