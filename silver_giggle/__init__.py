import time
from silver_giggle.celery_app import init_producer, init_consumer, init_consumer2

# producer celery app
producer = init_producer()

# consumer celery app
consumer = init_consumer()

consumer2 = init_consumer2()
