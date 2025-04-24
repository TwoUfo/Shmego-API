from flask import request, jsonify
from flask_restx import Resource
from .models import Car, ParkingSpot, ParkingSession
from .schemas import get_car_model, get_parking_spot_model

from api import db
from api.parking import ns


@ns.route("/cars")
class CarResource(Resource):
    def get(self):
        cars = Car.query.all()
        return jsonify([{"id": car.id, "license_plate": car.license_plate} for car in cars])

    @ns.expect(get_car_model(ns))
    def post(self):
        data = request.get_json()
        new_car = Car(
            license_plate=data.get("license_plate"),
            brand=data.get("brand"),
            model=data.get("model"),
            owner=data.get("owner")
        )
        db.session.add(new_car)
        db.session.commit()
        return jsonify({"message": "Car added", "car_id": new_car.id})
    

@ns.route("/cars/<string:car_license_plate>")
class CarDetailResource(Resource):
    def get(self, car_license_plate):
        car = Car.query.filter_by(license_plate=car_license_plate).first_or_404()
        return {
            "id": car.id,
            "license_plate": car.license_plate,
            "brand": car.brand,
            "model": car.model,
            "owner": car.owner
        }
    
    @ns.expect(get_car_model(ns))
    def put(self, car_license_plate):
        data = request.get_json()
        car = Car.query.get_or_404(car_license_plate)
        car.license_plate = data.get("license_plate", car.license_plate)
        car.brand = data.get("brand", car.brand)
        car.model = data.get("model", car.model)
        car.owner = data.get("owner", car.owner)
        db.session.commit()
        return jsonify({"message": "Car updated"})


@ns.route("/spots")
class ParkingSpotResource(Resource):
    def get(self):
        spots = ParkingSpot.query.all()
        return jsonify([{"id": spot.id, "number": spot.number} for spot in spots])

    @ns.expect(get_parking_spot_model(ns))
    def post(self):
        data = request.get_json()
        new_spot = ParkingSpot(
            number=data.get("number"),
            is_occupied=data.get("is_occupied", False)
        )
        db.session.add(new_spot)
        db.session.commit()
        return jsonify({"message": "Parking spot added", "spot_id": new_spot.id})
    
    
@ns.route("/spots/<string:spot_number>")
class ParkingSpotDetailResource(Resource):
    def get(self, spot_number):
        spot = ParkingSpot.query.filter_by(number=spot_number).first_or_404()
        return {
            "id": spot.id,
            "number": spot.number,
            "is_occupied": spot.is_occupied
        }
    
    @ns.expect(get_parking_spot_model(ns))
    def put(self, spot_number):
        data = request.get_json()
        spot = ParkingSpot.query.get_or_404(spot_number)
        spot.number = data.get("number", spot.number)
        spot.is_occupied = data.get("is_occupied", spot.is_occupied)
        db.session.commit()
        return jsonify({"message": "Parking spot updated"})