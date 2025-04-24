from flask import request, jsonify
from flask_restx import Resource
from .models import Car
from .schemas import get_car_model

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
    

@ns.route("/cars/<int:car_id>")
class CarDetailResource(Resource):
    def get(self, car_id):
        car = Car.query.get_or_404(car_id)
        return jsonify({"id": car.id, "license_plate": car.license_plate})
    
    @ns.expect(get_car_model(ns))
    def put(self, car_id):
        data = request.get_json()
        car = Car.query.get_or_404(car_id)
        car.license_plate = data.get("license_plate", car.license_plate)
        car.brand = data.get("brand", car.brand)
        car.model = data.get("model", car.model)
        car.owner = data.get("owner", car.owner)
        db.session.commit()
        return jsonify({"message": "Car updated"})
