import os
from flask import Flask, render_template, redirect, url_for
from database import load_movies, insert_user_info, get_user_by_email
from forms import SignupForm, LoginForm #import signupform func from forms.py
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

#app.config['SECRET_KEY'] = os.environ['secret_key']  #required for form validation
app.config['WTF_CSRF_ENABLED'] = False
csrf = CSRFProtect(app)

@app.route('/')  #home
def home():
  return render_template('home.html')


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
            print("login successfull")
          
            return redirect(url_for('home'))
        else:
            print("Invalid email or password!")
            
    return render_template('login.html', title='Log In', form=form)

@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list)


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
