from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SampleForm(FlaskForm):
	field = StringField("FieldName", validators=[DataRequired(), Length(min=5)])
	submit = SubmitField("Submit")

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Log in")