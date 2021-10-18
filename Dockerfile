FROM python:3.9-slim-buster

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY config.py wsgi.py ./
COPY up ./up 

CMD flask run --host=0.0.0.0