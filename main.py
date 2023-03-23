import os
from flask import Flask, render_template
from database import load_movies
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['secret_key'] #required for form validation
 

@app.route('/') #home
def home():
  return render_template('home.html')


@app.route('/signup') #signup
def sign_up():
  return render_template('signup.html')

@app.route('/shows')
def shows():
  # Fetch all movies from the database
  movies_list = load_movies()
  return render_template('shows.html', movies=movies_list)


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
