#!/bin/bash

# inspired by https://testdriven.io/courses/flask-celery/docker/
set -o errexit
set -o nounset

worker_ready() {
		celery -A wsgi.celery inspect ping
}

if [ "$#" -ne 1 ]; then
	echo "Usage: start.sh [flask|beat|worker|flower]"
	exit 1
else
	case $1 in
		flask)
			set -o pipefail
			flask run --host=0.0.0.0
			;;
		beat)
			celery -A wsgi.celery beat -l info -s /celerybeat-schedule.db --pidfile /celerybeat.pid
			;;
		worker)
			celery -A wsgi.celery worker -l info
			;;
		flower)
			until worker_ready; do >&2 echo 'Celery workers not available'; sleep 1; done
			>&2 echo 'Celery workers is available'
			celery -A wsgi.celery --broker="${CELERY_BROKER_URL}" flower
			;;
		*)
			echo "Usage: start.sh [flask|beat|worker|flower]"
			exit 1
			;;
	esac
fi