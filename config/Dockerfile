FROM python:3.6-slim

RUN apt-get update \
    && apt-get -y --no-install-recommends install \
        build-essential \
        curl \
        git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY Makefile setup.py /var/app/
COPY config /var/app/config

WORKDIR /var/app

RUN make build

CMD ["bash"]
