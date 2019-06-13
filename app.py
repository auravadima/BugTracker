from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import SampleForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd1b90a924a72bbe52b1f9fc45daae235'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	image = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	comments = db.relationship('Comment', backref='author', lazy=True)
	worklogs = db.relationship('WorkLog', backref='author', lazy=True)
	tasks = db.relationship('Task', backref='assigned', lazy=True)

	def __repr__(self):
		return f'User({self.id} {self.username} {self.image} {self.password})'

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'Comment({self.id} {self.date} {self.user_id})'

class WorkLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'Comment({self.id} {self.date} {self.user_id})'

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	type_id = db.Column(db.Integer, db.ForeignKey('task_type.id'), nullable=False)

	def __repr__(self):
		return f'{self.id} {self.title} {self.iser_id} {self.type_id}'

class TaskType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	taskname = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f'{self.id} {self.name}'

@app.route("/")
def index():
	return render_template('home.html')

@app.route('/form', methods=["POST", "GET"])
def form():
	form = SampleForm()
	if form.validate_on_submit():
		if form.field.data == "admin":
			flash("You are admin", category="success")
		else:
			flash("Go out", category="danger")
		return redirect(url_for('index'))
	return render_template('form.html', form=form)


if __name__ == '__main__':
	app.run(debug=True)