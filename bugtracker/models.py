from datetime import datetime
from bugtracker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	image = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	comments = db.relationship('Comment', backref='author', lazy=True)
	worklogs = db.relationship('WorkLog', backref='author', lazy=True)
	tasks = db.relationship('Task', backref='assigned', lazy=True)

	def __repr__(self):
		return f'User({self.id} {self.username} {self.image} {self.password})'

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	description = db.Column(db.Text, nullable=False)
	tasks = db.relationship('Task', backref='project', lazy=True)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


	def __repr__(self):
		return f'Comment({self.id} {self.date} {self.user_id})'

class WorkLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

	def __repr__(self):
		return f'Comment({self.id} {self.date} {self.user_id})'

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	comments = db.relationship('Comment', backref='task', lazy=True)
	worklogs = db.relationship('WorkLog', backref='task', lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
	type_id = db.Column(db.Integer, db.ForeignKey('task_type.id'), nullable=False)

	def __repr__(self):
		return f'{self.id} {self.title} {self.iser_id} {self.type_id}'

class TaskType(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	taskname = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f'{self.id} {self.name}'