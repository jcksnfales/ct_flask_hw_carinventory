from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/cars', methods = ['POST'])
@token_required
def add_car(current_user_token):
    nickname = request.json['nickname']
    make = request.json['make']
    model = request.json['model']
    prodyear = request.json['prodyear']
    mileage = request.json['mileage']
    user_token = current_user_token.token

    new_car = Car(nickname, make, model, prodyear, mileage, user_token=user_token)

    db.session.add(new_car)
    db.session.commit()

    response = car_schema.dump(new_car)
    return jsonify(response)