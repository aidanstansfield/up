from celery import shared_task
from . import ext_celery, db
from .models import Endpoint, Available
import requests
from flask import current_app

print('###########################################')
print(ext_celery.celery)
print('###########################################')

# celery = ext_celery.celery

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# 	sender.add_periodic_task(60, check_enabled(), name='Check the enabled endpoints')

# @celery.on_after_finalize.connect
# def setup_periodic_tasks():
	#celery.add_periodic_task(60, check_enabled(), name='Check the enabled endpoints')
	#sender.add_periodic_task(60, check_enabled(), name='Check the enabled endpoints')

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
	db.session.commit()