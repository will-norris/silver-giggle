.PHONY: build producer consumer beat

build:
	pip install -e .

producer:
	celery -A silver_giggle.producer -Q silver_giggle.producer worker

consumer:
	celery -A silver_giggle.consumer worker

beat:
	celery -A silver_giggle.producer beat
