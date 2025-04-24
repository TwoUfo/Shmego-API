from flask import request, jsonify
from flask_restx import Resource
from .models import Car, ParkingSpot, ParkingSession
from .schemas import get_car_model, get_parking_spot_model, get_session_model
from datetime import datetime

from api import db
from api.parking import ns


@ns.route("/cars")
class CarResource(Resource):
    def get(self):
        cars = Car.query.all()
        return jsonify([{"license_plate": car.license_plate} for car in cars])

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
        return jsonify({"message": "Car added"})
    

@ns.route("/cars/<string:car_license_plate>")
class CarDetailResource(Resource):
    def get(self, car_license_plate):
        car = Car.query.filter_by(license_plate=car_license_plate).first_or_404()
        return {
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
        return jsonify([{"number": spot.number} for spot in spots])

    @ns.expect(get_parking_spot_model(ns))
    def post(self):
        data = request.get_json()
        new_spot = ParkingSpot(
            number=data.get("number"),
            is_occupied=data.get("is_occupied", False)
        )
        db.session.add(new_spot)
        db.session.commit()
        return jsonify({"message": "Parking spot added"})
    
    
@ns.route("/spots/<string:spot_number>")
class ParkingSpotDetailResource(Resource):
    def get(self, spot_number):
        spot = ParkingSpot.query.filter_by(number=spot_number).first_or_404()
        return {
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
    

@ns.route("/sessions")
class ParkingSessionResource(Resource):
    def get(self):
        sessions = ParkingSession.query.all()
        return jsonify([{"id": session.id, "car_id": session.car_id, "spot_id": session.spot_id} for session in sessions])


@ns.route("/sessions/<int:session_id>")
class ParkingSessionDetailResource(Resource):
    def get(self, session_id):
        session = ParkingSession.query.get_or_404(session_id)
        return {
            "id": session.id,
            "car_id": session.car_id,
            "spot_id": session.spot_id,
            "check_in_time": session.check_in_time,
            "check_out_time": session.check_out_time,
            "cost": session.cost
        }

@ns.route("/sessions/check-in")
class SessionsCheckInResource(Resource):
    @ns.expect(get_session_model(ns))
    def post(self):
        data = request.get_json()
        spot = ParkingSpot.query.filter_by(number=data.get("spot_number")).first_or_404()
        
        if spot.is_occupied:
            return jsonify({"error_message": "Parking spot is already occupied"})

        new_session = ParkingSession(
            car_id=data.get("car_license_plate"),
            spot_id=data.get("spot_number"),
            check_in_time=data.get("check_in_time"),
            check_out_time=None,
            
        )
        spot.is_occupied = True
        
        db.session.add(new_session)
        db.session.commit()
        return jsonify({"message": "Parking session started", "session_id": new_session.id})
    

@ns.route("/sessions/check-out/<string:car_license_plate>")
class SessionsCheckOutResource(Resource):
    def post(self, car_license_plate):
        session = ParkingSession.query.filter_by(car_id=car_license_plate).first_or_404()
        
        if session.check_out_time is not None:
            return {"error": "Already checked out."}, 400

        session.check_out_time = datetime.now()
        duration = session.check_out_time - session.check_in_time
        hours = max(1, int(duration.total_seconds() // 3600))
        session.cost = hours * 5

        session.spot.is_occupied = False
        db.session.commit()
        return {
            "message": "Checked out successfully.",
            "cost": session.cost,
            "duration_hours": hours
        }