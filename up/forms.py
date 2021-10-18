from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import current_user

class SignupForm(FlaskForm):
	"""User Sign-up Form."""
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[
		Length(min=6), 
		Email(message='Enter a valid email.'), 
		DataRequired()
	])
	password = PasswordField('Password', validators=[DataRequired(), 
		Length(min=6, message='Select a stronger password.')
	])
	confirm = PasswordField('Confirm Your Password', validators=[DataRequired(),
		EqualTo('password', message='Passwords must match.')
	])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	"""User Log-in Form."""
	email = StringField('Email', validators=[DataRequired(),
		Email(message='Enter a valid email.')
	])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Log In')

class AlertForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	method = SelectField("Method", choices=[(None, 'Please select a method'), ('slack', 'Slack')], validators=[DataRequired(), AnyOf(['slack'])])
	target = StringField('Target', validators=[DataRequired(), URL()])
	submit = SubmitField('Create alert')

class EndpointForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	method = SelectField('Method', choices=[(None, 'Please select a method'), ('http', 'HTTP'), ('https', 'HTTPS')], validators=[DataRequired(), AnyOf(['http', 'https'])])
	endpoint = StringField('Endpoint', validators=[DataRequired(), URL()])
	enabled = BooleanField("Enabled", validators=[DataRequired()], default="checked")
	alert = QuerySelectField(query_factory=lambda: current_user.alerts, get_label="name")
	submit = SubmitField('Create alert')