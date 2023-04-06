import os
import requests
from flask import Flask, render_template, redirect, url_for, session, request
from database import load_movies, insert_user_info, get_user_by_email
from forms import SignupForm, LoginForm  #import signupform func from forms.py
#from flask_login import UserMixin , login_user , LoginManager , login_required , logout_user , current_user 
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import stripe

app = Flask(__name__)


app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ['secret_key']  #required for form validation
#app.config['SECRET_KEY'] = 'my_secret_key'
Session(app)

#public_key = "pk_test_6pRNASCoBOKtIshFeQd4XMUh"
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

app.config['WTF_CSRF_ENABLED'] = False

csrf = CSRFProtect(app)

  
@app.route('/')  #home
def home():
  card_data = load_movies()
  username = session.get('username')
  if username:
      print(username)
  return render_template('home.html', data=card_data, username = username)

@app.route('/checkout_2') 
def checkout_2():
  
  return render_template('checkout_2.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():

    # use the file object in your product creation
    try:
        product = stripe.Product.create(
            name="My Product",
            description="Product description",
            
        )

        price = stripe.Price.create(
            unit_amount=2948,
            currency="usd",
            product=product.id,
            
        )

        print("Product and price created successfully.")
    except stripe.error.InvalidRequestError as e:
        print(e)

    print("Failed to create file object in Stripe.")

    
    # Create a Checkout session using the Price object
    try:
        quantity = int(request.form['quantity'])
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price.id,
                    'quantity': quantity,
                    #'images': [product_image.id],
                },
            ],
            
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
            
        )
    except Exception as e:
        return str(e)

    # Redirect the customer to the checkout page
    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    return '<h1>Payment successful!</h1>'

@app.route('/cancel')
def cancel():
    return '<h1>Payment cancelled.</h1>'
  
'''
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html', public_key = public_key)

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    # PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999, # 19.99
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('thankyou'))
'''

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
    user = get_user_by_email(email)
    if user == False and insert_user_info(name, email, password):
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
      session['user_id'] = user['id']
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
    session.pop('user_id', None)
    
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
