from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

# ADD NEW CAR
@api.route('/cars', methods=['POST'])
@token_required
def add_car(current_user_token):
    user_token = current_user_token.token
    nickname = request.json['nickname']
    make = request.json['make']
    model = request.json['model']
    prodyear = request.json['prodyear']
    mileage = request.json['mileage']

    new_car = Car(nickname, make, model, prodyear, mileage, user_token=user_token)

    db.session.add(new_car)
    db.session.commit()

    return jsonify(car_schema.dump(new_car))

# GET ALL CARS
@api.route('/cars', methods=['GET'])
@token_required
def get_contact(current_user_token):
    user_token = current_user_token.token
    cars = Car.query.filter_by(user_token=user_token).all()
    return jsonify(cars_schema.dump(cars))