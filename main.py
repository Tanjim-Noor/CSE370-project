from flask import Flask, render_template

app = Flask(__name__)


@app.route('/') #home
def home():
  return render_template('home.html')


@app.route('/signup') #signup
def sign_up():
  return render_template('signup.html')

@app.route('/shows')
def shows():
  return render_template('shows.html')


if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True)
