from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired()])
  email = StringField(label='Email', validators=[DataRequired(), Email()])
  pass1 = PasswordField(label='Password', validators=[DataRequired()])
  pass2 = PasswordField(label='Confirm Password', validators=[DataRequired()])
  submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember me')
  submit = SubmitField('Log In')