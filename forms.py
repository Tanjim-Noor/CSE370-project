from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
  username = StringField(label = 'Username', validators = [DataRequired()])
  email = StringField(label = 'Email', validators = [DataRequired()])
  pass1 = PasswordField(label = 'Password', validators = [DataRequired()])
  pass2 = PasswordField(label = 'Confirm Password', validators = [DataRequired()])
  submit = SubmitField(label = 'submit')