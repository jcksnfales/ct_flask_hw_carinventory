from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

# ADD NEW CAR
@api.route('/cars', methods=['POST'])
@token_required
def add_car(current_user_token):
    nickname = request.json['nickname']
    make = request.json['make']
    model = request.json['model']
    prodyear = request.json['prodyear']
    mileage = request.json['mileage']

    new_car = Car(current_user_token.token, nickname, make, model, prodyear, mileage)

    db.session.add(new_car)
    db.session.commit()

    return jsonify(car_schema.dump(new_car))

# GET ALL CARS
@api.route('/cars', methods=['GET'])
@token_required
def get_all(current_user_token):
    current_cars = Car.query.filter_by(user_token=current_user_token.token).all()
    return jsonify(cars_schema.dump(current_cars))

# GET SPECIFIC CAR
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_from_id(current_user_token, id):
    current_car = Car.query.get(id)
    return jsonify(car_schema.dump(current_car))

# POST/PUT CAR
@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_id(current_user_token, id):
    # find car by id
    updated_car = Car.query.get(id)
    # check car's recorded user_token against given user token
    if current_user_token.token == updated_car.user_token:
        # if user tokens match, update the data
        updated_car.nickname = request.json['nickname']
        updated_car.make = request.json['make']
        updated_car.model = request.json['model']
        updated_car.prodyear = request.json['prodyear']
        updated_car.mileage = request.json['mileage']
        # then return the data of the changed car
        return jsonify(car_schema.dump(updated_car))
    else:
        # if user tokens do not match, return user an error message
        return jsonify({'message': 'Given car does not belong to given access token'})