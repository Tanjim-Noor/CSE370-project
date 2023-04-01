import os
from flask import Flask, render_template, redirect, url_for, session, flash
from database import load_movies, insert_user_info, get_user_by_email
from forms import SignupForm, LoginForm  #import signupform func from forms.py
#from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user 
from flask_wtf.csrf import CSRFProtect
from flask_session import Session


app = Flask(__name__)


app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'my_secret_key'
Session(app)

#app.config['SECRET_KEY'] = os.environ['secret_key']  #required for form validation
app.config['WTF_CSRF_ENABLED'] = False
csrf = CSRFProtect(app)

  
@app.route('/')  #home
def home():
  card_data = load_movies()
  username = session.get('username')
  if username:
      print(username)
  return render_template('home.html', data=card_data, username = username)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  name = None
  form = SignupForm()

  if form.validate_on_submit():
    name = form.username.data
    email = form.email.data
    password = form.pass1.data
    form.username.data = ''
    form.email.data = ''
    form.pass1.data = ''
    form.pass2.data = ''
    if insert_user_info(name, email, password):
      print(f'Signup Succesful for {name} ')
      return redirect(url_for('signup_success', name=name))
    else:
      #flash('Username or email already exists!', 'danger')
      print("not successful")
  else:
    print(form.errors)

  return render_template('signup.html', name=name, form=form)


@app.route('/signup/success/<string:name>')
def signup_success(name):
  print("Sign up success")
  return render_template('signup_success.html', name=name)


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    user = get_user_by_email(email)

    if user and user['password'] == password:
      session['username'] = user['username']
      print("login successfull")
      #print(session['username'])

      return redirect(url_for('home'))
    else:
      print("Invalid email or password!")

  return render_template('login.html', title='Log In', form=form)

@app.route('/log_out')
def log_out():
  # Remove the user's session data
    session.pop('username', None)
    
    # Redirect the user to the home page
    return redirect(url_for('home'))
  


@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list)


@app.route('/user-profile')
def user_profile():
  return render_template('user-profile.html')


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
