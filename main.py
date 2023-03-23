import os
from flask import Flask, render_template, redirect, url_for
from database import load_movies
from forms import SignupForm, LoginForm #import signupform func from forms.py
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

#app.config['SECRET_KEY'] = os.environ['secret_key']  #required for form validation
app.config['WTF_CSRF_ENABLED'] = False
csrf = CSRFProtect(app)

@app.route('/')  #home
def home():
  return render_template('home.html')


@app.route('/sign_up', methods=['GET', 'POST'])  #signup
def sign_up():
  name = None
  form = SignupForm()

  if form.validate_on_submit():
    name = form.username.data
    form.username.data = ''
    print(f'Signup Succesful for {name} ')  #doesn't work idk why
    return redirect(url_for('signup_success', name=name))

  else:
    print(form.errors)  # print the validation errors
    print("not successful")

  return render_template('signup.html', name=name, form=form)


@app.route('/signup/success/<string:name>')
def signup_success(name):
  print("Sign up success")
  return render_template('signup_success.html', name=name)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        # handle login logic here
        flash('You have been logged in successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Log In', form=form)

@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list)


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
