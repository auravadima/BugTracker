from flask import render_template, flash, redirect, url_for, request
from bugtracker import app
from bugtracker import db
from bugtracker.models import User, Comment, WorkLog, Task
from bugtracker.forms import LoginForm, RegisterForm
from bugtracker import bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps

def authorize(f):
	@wraps(f)
	def check_auth():
		if not current_user.is_authenticated:
			flash("You need to login first", category='danger')
			return redirect(url_for('login'))
		return f()
	return check_auth

@app.route("/")
def index():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	return redirect(url_for('dashboard'))

@app.route("/dashboard")
@authorize
def dashboard():
	return render_template('dashboard.html', title='Dashboard')

@app.route("/projects")
@authorize
def projects():
	return render_template('projects.html', title='Projects')

@app.route('/login', methods=["POST", "GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		print(user)
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=True)
			flash('You logged in!', category='success')
			return redirect(url_for('dashboard'))
		else:
			flash("Login unsuccessful. Check username and password", category="danger")
	return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=["POST", "GET"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("Account has been created", category="success")
		return redirect(url_for('login'))
	return render_template('register.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))