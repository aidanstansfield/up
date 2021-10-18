# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db, login_manager
from .forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login', next=request.endpoint))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.check_password(password=form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			if next_page: return redirect(url_for(next_page))
			return redirect(url_for('main.index'))
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login'))
	return render_template('login.html', form=form) 

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	if form.validate_on_submit():
		existing_user = User.query.filter_by(email=form.email.data).first()
		if existing_user is None:
			user = User(name=form.name.data, email=form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()  # Create new user
			login_user(user)  # Log in as newly created user
			return redirect(url_for('main.index'))
		flash('A user already exists with that email address.')
	return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/update_details', methods=['GET', 'POST'])
@login_required
def update_details():
	if request.method == 'POST':
		name = request.form.get('name')
		current_user.name = name
		db.session.commit()
		return redirect(url_for('main.profile'))
	return render_template('update_details.html')