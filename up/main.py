# main.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from wtforms.fields.core import Label
from .forms import AlertForm, EndpointForm
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)

@main.route('/alerts', methods=['GET'])
@login_required
def get_alerts():
	alerts = current_user.alerts
	return render_template('alerts.html', alerts=alerts, heading='Alerts')

@main.route('/alerts/<int:alert_id>', methods=['GET', 'POST'])
@login_required
def get_alert(alert_id):
	alert = Alert.query.filter_by(id=alert_id).first()
	if alert is None or alert.user_id != current_user.id:
		flash('The alert does not exist, or it does not belong to you!')
		return render_template('alert.html'), 403
	form = AlertForm(obj=alert)
	if form.validate_on_submit():
		form.populate_obj(alert)
		db.session.commit()
		return redirect(url_for('main.get_alerts'))
	form.submit.label = Label(form.submit.id, 'Update alert')
	return render_template('alert.html', form=form, alert_id=alert_id)

@main.route('/alerts/new', methods=['GET', 'POST'])
@login_required
def new_alert():
	form = AlertForm()
	if form.validate_on_submit():
		alert = Alert(name=form.name.data, method=form.method.data, 
		target=form.target.data, user_id=current_user.id)
		db.session.add(alert)
		db.session.commit()
		return redirect(url_for('main.get_alerts'))
	return render_template('alert.html', form=form)

@main.route('/endpoints', methods=['GET'])
@login_required
def get_endpoints():
	endpoints = current_user.endpoints
	return render_template('endpoints.html', endpoints=endpoints, heading='Endpoints')

@main.route('/endpoints/<int:endpoint_id>', methods=['GET', 'POST'])
@login_required
def get_endpoint(endpoint_id):
	endpoint = Endpoint.query.filter_by(id=endpoint_id).first()
	if endpoint is None or endpoint.user_id != current_user.id:
		flash('The alert does not exist, or it does not belong to you!')
		return render_template('endpoint.html'), 403
	form = EndpointForm(obj=endpoint)
	if form.validate_on_submit():
		form.populate_obj(endpoint)
		db.session.commit()
		return redirect(url_for('main.get_endpoints'))
	form.submit.label = Label(form.submit.id, 'Update endpoint')
	return render_template('endpoint.html', form=form, endpoint_id=endpoint_id)

@main.route('/endpoint/new', methods=['GET', 'POST'])
@login_required
def new_endpoint():
	form = EndpointForm()
	if form.validate_on_submit():
		endpoint = Endpoint(name=form.name.data, method=form.method.data, 
		endpoint=form.endpoint.data, user_id=current_user.id, 
		alert_id=form.alert.data.id, enabled=form.enabled.data)
		db.session.add(endpoint)
		db.session.commit()
		return redirect(url_for('main.get_endpoints'))
	alerts = current_user.alerts
	return render_template('endpoint.html', form=form, alerts=alerts)