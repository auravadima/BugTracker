from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from bugtracker.models import User

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField("Confirm", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Register")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is taken. Please choose another one.')