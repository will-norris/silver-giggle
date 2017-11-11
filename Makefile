.PHONY: build producer consumer beat

build:
	pip install -e .

producer:
	celery -A silver_giggle.producer.app -Q silver_giggle.producer worker

consumer:
	celery -A silver_giggle.consumer.app worker

beat:
	celery -A silver_giggle.producer.app beat
