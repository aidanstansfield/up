# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(321), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String())

class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.column(db.Integer, db.ForeignKey(User.id), nullable=False)
	method = db.column(db.String)