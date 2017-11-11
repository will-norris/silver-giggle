.PHONY: build producer consumer beat

build:
	pip install -e .

producer:
	celery -A silver_giggle.producer worker

consumer:
	celery -A silver_giggle.consumer worker

consumer2:
	celery -A silver_giggle.consumer2 worker

beat:
	celery -A silver_giggle.producer beat
