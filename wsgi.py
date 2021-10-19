#!/usr/bin/env python3
from celery.signals import worker_process_init
from up import create_app, ext_celery, db

app = create_app()
app.app_context().push()

# celery
celery = ext_celery.celery

# entry point for uWSGI
if __name__ == "__main__":
	app.run()