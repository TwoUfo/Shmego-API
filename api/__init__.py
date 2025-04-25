from flask import Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint)
db = SQLAlchemy()

from api.parking import ns as pk_ns
from api.parking.models import Car, ParkingSession, ParkingSpot

api.add_namespace(pk_ns, path="/parking")
