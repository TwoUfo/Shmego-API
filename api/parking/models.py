from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api import db


class Car(db.Model):
    license_plate = db.Column(db.String(20), primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    owner = db.Column(db.String(100))


class ParkingSpot(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    is_occupied = db.Column(db.Boolean, default=False)


class ParkingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_license_plate = db.Column(db.String(20), db.ForeignKey('car.license_plate'))
    spot_number = db.Column(db.Integer, db.ForeignKey('parking_spot.number'))
    check_in_time = db.Column(db.DateTime, default=datetime.now)
    check_out_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)

    car = db.relationship('Car')
    spot = db.relationship('ParkingSpot')
