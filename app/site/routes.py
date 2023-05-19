from flask import Blueprint, render_template, redirect
from flask_login import current_user
from models import Car, car_schema, cars_schema

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def landing():
    return render_template('index.html')

@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, query the database for cars owned by them
        queried_cars = Car.query.filter_by(user_token=current_user.token).all()
        # direct the user to /profile, passing in their cars as 'user_cars' and the cars' schema dumps as 'user_cars_json'
        return render_template('profile.html', user_cars=queried_cars, user_cars_json=cars_schema.dump(queried_cars))
    else:
        # otherwise, redirect them to the landing page
        return redirect('/')