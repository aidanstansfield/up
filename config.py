#!/usr/bin/env python3

from os import environ
from dotenv import load_dotenv, find_dotenv

class Config:
	if find_dotenv() == '':
		# could not find a dotenv file, use development defaults
		# NOTE: These are dev defaults, these creds/keys are not used in prod

		# General
		SECRET_KEY = b'pf\x95\x11\x95s\x9c\xcd>\x8bgj\xd3\x15f\x08' # os.urandom(16)
		FLASK_ENV = environ.get("FLASK_ENV", "development")

		# Database
		SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite:///dev.db") # 'sqlite:///dev.db'
		SQLALCHEMY_TRACK_MODIFICATIONS = False
	else:
		load_dotenv()
		SECRET_KEY = environ.get("SECRET_KEY")
		FLASK_ENV = 'production'
		# Database
		SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
		SQLALCHEMY_TRACK_MODIFICATIONS = False
