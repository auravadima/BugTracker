from unittest import TestCase
from bugtracker import db
from bugtracker import User, Comment, Task, TaskType, WorkLog
from datetime import datetime

class UserTests(TestCase):

	@classmethod
	def setUpClass(self):
		db.drop_all()
		db.create_all()

		us = User(username='vadim', image='pic.jpg', password='qwerty')
		db.session.add(us)

		us = User(username='test', password='test')
		db.session.add(us)

		us = User(username='test', password='qweqwq')

		db.session.commit()

	def test_user_created(self):
		user = User.query.filter_by(username='vadim').first()
		self.assertIsNotNone(user, msg='User did\'n created')

	def test_user_default_image(self):
		user = User.query.filter_by(username='test').first()
		image = user.image
		self.assertEqual('default.jpg', image, msg='user did\'n created with default image')

	def test_unique_username(self):
		users = User.query.filter_by(username='test')
		count = users.count()
		self.assertEqual(1, count, msg='More than one user with the same name')

class CommentTests(TestCase):

	@classmethod
	def setUpClass(self):
		db.drop_all()
		db.create_all()

		us = User(username='vadim', password='test')
		db.session.add(us)

		comment = Comment(content='some content', user_id=1)
		db.session.add(comment)

		comment = Comment(content='another content', user_id=1)
		db.session.add(comment)

		db.session.commit()

	def test_comment_created(self):
		comment = Comment.query.first()
		self.assertIsNotNone(comment, msg='Comment did\'t created')

	def test_comment_has_author(self):
		comment = Comment.query.filter_by(content='some content').first()
		user = comment.author
		self.assertEqual('vadim', user.username, msg='Comment has wrong author')

	def test_comments_with_same_author(self):
		comments = Comment.query.filter_by(user_id=1)
		count = comments.count()
		self.assertGreater(count, 1, msg='Only one comment with same author')

class WorkLogTests(TestCase):

	@classmethod
	def setUpClass(self):
		db.drop_all()
		db.create_all()

		us = User(username='vadim', password='test')
		db.session.add(us)

		worklog = WorkLog(content='some content', user_id=1)
		db.session.add(worklog)

		worklog = WorkLog(content='another content', user_id=1)
		db.session.add(worklog)

		self.date = datetime.utcnow()
		worklog = WorkLog(content='log with date', date=self.date, user_id=1)

		db.session.commit()

	def test_worklog_created(self):
		worklog = WorkLog.query.first()
		self.assertIsNotNone(worklog, msg='worklog did\'t created')

	def test_worklog_has_author(self):
		worklog = WorkLog.query.filter_by(content='some content').first()
		user = worklog.author
		self.assertEqual('vadim', user.username, msg='worklog has wrong author')

	def test_worklogs_with_same_author(self):
		worklogs = WorkLog.query.filter_by(user_id=1)
		count = worklogs.count()
		self.assertGreater(count, 1, msg='Only one worklog with same author')

	def test_worklog_has_date(self):
		worklog = WorkLog.query.filter_by(date=self.date).first()
		self.assertIsNone(worklog)

	def test_all_worklogs_has_date(self):
		worklogs = WorkLog.query.all()
		dates = [log.date for log in worklogs]
		self.assertTrue(all(dates), msg='Some worklogs has no date')

class TaskTests(TestCase):

	@classmethod
	def setUpClass(self):
		db.drop_all()
		db.create_all()

		us = User(username='vadim', password='test')
		db.session.add(us)

		worklog = WorkLog(content='some content', user_id=1)
		db.session.add(worklog)

		worklog = WorkLog(content='another content', user_id=1)
		db.session.add(worklog)

		self.date = datetime.utcnow()
		worklog = WorkLog(content='log with date', date=self.date, user_id=1)

		db.session.commit()