#!/usr/bin/env python3

from os import environ
from dotenv import load_dotenv, find_dotenv

class BaseConfig:
	# SQLAlchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///dev.db")

	# Celery
	CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
	CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

class DevelopmentConfig(BaseConfig):
	FLASK_ENV = "development"
	SECRET_KEY = b'pf\x95\x11\x95s\x9c\xcd>\x8bgj\xd3\x15f\x08'
	DEBUG = True

class ProductionConfig(BaseConfig):
		if find_dotenv != '': load_dotenv()
		SECRET_KEY = environ.get("SECRET_KEY")
		FLASK_ENV = 'production'

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
