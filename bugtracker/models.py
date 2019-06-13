from datetime import datetime
from bugtracker import db

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