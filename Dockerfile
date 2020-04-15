FROM python:3.6

COPY requirements.txt /tmp/
RUN pip install -U pip; \
	pip install -r /tmp/requirements.txt

COPY app /app

WORKDIR /app
