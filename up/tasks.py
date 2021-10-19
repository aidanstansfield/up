from celery import shared_task
from celery.signals import worker_process_init
from . import ext_celery, db
from .models import Endpoint, Available, Alert
import requests
import urllib3
from flask import current_app as app

urllib3.disable_warnings()

celery = ext_celery.celery

# this is better practice, but doesn't work.
# @celery.on_after_configure.connect
# def setup_periodic_tasks(**kwargs):
# 	celery.add_periodic_task(10, check_enabled(), name='check_enabled')

# manually set schedule works
celery.conf.beat_schedule = {
	'check_enabled': {
		'task': 'up.tasks.check_enabled',
		'schedule': 20.0
	},
}

# from https://stackoverflow.com/questions/43944787/sqlalchemy-celery-with-scoped-session-error
@worker_process_init.connect
def prep_db_pool(**kwargs):
	"""
	When Celery fork's the parent process, the db engine & connection pool is included in that.
	But, the db connections should not be shared across processes, so we tell the engine
	to dispose of all existing connections, which will cause new ones to be opened in the child
	processes as needed.
	More info: https://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing
	"""
	with app.app_context():
		db.engine.dispose()

@shared_task
def check_endpoint(endpoint_id, method, url):
	if method.lower() in ['http', 'https']:
		return (endpoint_id, requests.get(url, verify=False, timeout=30).status_code == 200)
	return (endpoint_id, False)

@shared_task
def check_enabled():
	enabled_endpoints = Endpoint.query.filter_by(enabled=True).all()
	for endpoint in enabled_endpoints:
		check_endpoint.apply_async((endpoint.id, endpoint.method, endpoint.endpoint), 
		expires=60, link=process_result.s())

@shared_task
def process_result(result):
	endpoint_id = result[0]
	available = result[1]
	av = Available(endpoint_id=endpoint_id, available=available)
	db.session.add(av)
	endpoint = Endpoint.query.filter_by(id=endpoint_id).first()
	if available and not endpoint.available:
		send_alert.delay(endpoint.alert.id, f"{endpoint.name} is UP")
		endpoint.available = available
	elif not available and endpoint.available:
		send_alert.delay(endpoint.alert.id, f"{endpoint.name} is DOWN")
		endpoint.available = available
	db.session.commit()

@shared_task
def send_alert(alert_id, alert_text):
	alert = Alert.query.filter_by(id=alert_id).first()
	if alert.method == "slack":
		requests.post(alert.target, json={'text': alert_text})