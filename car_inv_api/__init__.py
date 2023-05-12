from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

car_inv_api = Flask(__name__)
CORS(car_inv_api)

car_inv_api.register_blueprint(site)
car_inv_api.register_blueprint(auth)
car_inv_api.register_blueprint(api)

car_inv_api.json_encoder = JSONEncoder
car_inv_api.config.from_object(Config)
root_db.init_app(car_inv_api)
login_manager.init_app(car_inv_api)
ma.init_app(car_inv_api)
migrate = Migrate(car_inv_api, root_db)