from flask import Flask
from flask_celeryext import FlaskCeleryExt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from os import environ
from config import config
from .celery_utils import make_celery

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)

def create_app(config_name=None):
	# instantiate app
	app = Flask(__name__, instance_relative_config=False)

	# Flask app config
	if config_name is None:
		config_name = environ.get("FLASK_CONFIG", "development")
	
	app.config.from_object(config[config_name])

	# set up extensions
	db.init_app(app)
	ext_celery.init_app(app)

	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	with app.app_context():
		# blueprint for auth routes in our app
		from .auth import auth as auth_blueprint
		app.register_blueprint(auth_blueprint)

		# blueprint for non-auth parts of app
		from .main import main as main_blueprint
		app.register_blueprint(main_blueprint)

		db.create_all()

		# tasks
		from . import tasks
		
		return app
