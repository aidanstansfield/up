from celery import shared_task
import requests

@shared_task
def check_endpoint(method, url):
	if method.lower() in ['http', 'https']:
		return requests.get(url).status_code == 200
	return False