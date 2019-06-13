from flask import render_template, flash, redirect, url_for
from bugtracker import app
from bugtracker.models import User, Comment, WorkLog, Task
from bugtracker.forms import LoginForm

@app.route("/")
def index():
	return render_template('dashboard.html', title='Dashboard')

@app.route('/login', methods=["POST", "GET"])
def form():
	form = LoginForm()
	if form.validate_on_submit():
		if form.field.data == "admin":
			flash("You are admin", category="success")
		else:
			flash("Go out", category="danger")
		return redirect(url_for('index'))
	return render_template('login.html', form=form)