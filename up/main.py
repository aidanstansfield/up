# main.py

from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
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
	return render_template('alerts.html', alerts=alerts)

@main.route('/alerts/<int:alert_id>', methods=['GET'])
@login_required
def get_alert(alert_id):
	alert = Alert.query.filter_by(id=alert_id).first()
	if alert is None or alert.user_id != current_user.id:
		flash('The alert does not exist, or it does not belong to you!')
		return render_template('alert.html'), 403
	return render_template('alert.html', alert=alert)

@main.route('/alerts/new', methods=['GET', 'POST'])
@login_required
def new_alert():
	name = request.form.get('name')
	method = request.form.get('method')
	if True: pass
	slack_url = request.form.get('slack_url')