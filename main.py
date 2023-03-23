import os
from flask import Flask, render_template
from database import load_movies
from forms import *
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['secret_key'] #required for form validation
 

@app.route('/') #home
def home():
  return render_template('home.html')


@app.route('/signup', methods = ['GET', 'POST']) #signup
def sign_up():
  name = None
  form = SignupForm()
  if form.validate_on_submit():
    name = form.name.data
    print(f'Signup Succesful for {name} ')
  return render_template('signup.html', form = form)

@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list)



if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
