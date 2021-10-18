# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from .forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()

	# check if user actually exists
	# take the user supplied password, hash it, and compare it to the hashed password in database
	if not user or not check_password_hash(user.password, password): 
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

	# if the above check passes, then we know the user has the right credentials
	login_user(user, remember=remember)
	return redirect(url_for('main.profile'))

# @auth.route('/signup')
# def signup():
# 	return render_template('signup.html')

# @auth.route('/signup', methods=['POST'])
# def signup_post():

# 	email = request.form.get('email')
# 	name = request.form.get('name')
# 	password = request.form.get('password')

# 	user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

# 	if user: # if a user is found, we want to redirect back to signup page so user can try again  
# 		flash('Email address already exists')
# 		return redirect(url_for('auth.signup'))

# 	# create new user with the form data. Hash the password so plaintext version isn't saved.
# 	new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

# 	# add the new user to the database
# 	db.session.add(new_user)
# 	db.session.commit()

# 	return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
	form = SignupForm()
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