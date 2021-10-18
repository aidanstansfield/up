# models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(321), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(), nullable=False)
	alerts = db.relationship('Alert', backref='user', lazy=True)
	endpoints = db.relationship('Endpoint', backref='user', lazy=True)

	def set_password(self, password):
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):
		return check_password_hash(self.password, password)

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(), nullable=False)	
	method = db.Column(db.String(), nullable=False) # slack, email etc.
	slack_url = db.Column(db.String())
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

class Endpoint(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(), nullable=False)
	method = db.Column(db.String(), nullable=False) # http, https [more]
	endpoint = db.Column(db.String(), nullable=False)
	enabled = db.Column(db.Boolean, nullable=False, default=True)
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	alert_id = db.Column(db.Integer, db.ForeignKey(Alert.id), nullable=False)

class Available(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	timestamp = db.Column(db.Time, nullable=False, default=func.now())
	available = db.Column(db.Boolean)
	endpoint_id = db.Column(db.Integer, db.ForeignKey(Endpoint.id), nullable=False)