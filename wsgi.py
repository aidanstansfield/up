#!/usr/bin/env python3
from up import create_app, ext_celery

app = create_app()
app.app_context().push()
celery = ext_celery.celery

# entry point for uWSGI
if __name__ == "__main__":
	app.run()