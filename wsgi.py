#!/usr/bin/env python3
from up import create_app

app = create_app()

# entry point for uWSGI
if __name__ == "__main__":
	app.run()