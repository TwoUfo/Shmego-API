from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    owner = db.Column(db.String(100))

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True)
    is_occupied = db.Column(db.Boolean, default=False)

class ParkingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    check_in_time = db.Column(db.DateTime, default=datetime.now)
    check_out_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)

    car = db.relationship('Car')
    spot = db.relationship('ParkingSpot')