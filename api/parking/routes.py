from flask import request
from flask_restx import Resource
from api.parking.models import Car, ParkingSpot, ParkingSession
from api.parking.schemas import get_car_model, get_parking_spot_model, get_session_model
from datetime import datetime
from api import db
from api.parking import ns
from api.utils import response
from api.parking.utils import calculate_cost, check_session_status, check_object_exists, check_is_spot_occupied
from api.parking.errors import SessionAlreadyCheckedOut, ObjectNotFound, SpotAlreadyOccupied
from utils.constants import *


@ns.route("/cars")
class Cars(Resource):
    def get(self):
        cars = Car.query.all()
        data = [{KEY_LICENSE_PLATE: car.license_plate, KEY_OWNER: car.owner} for car in cars]
        
        return response(data=data, status_code=200)

    @ns.expect(get_car_model(ns))
    def post(self):
        try:
            data = request.get_json()
            new_car = Car(
                license_plate=data.get(KEY_LICENSE_PLATE),
                brand=data.get(KEY_BRAND),
                model=data.get(KEY_MODEL),
                owner=data.get(KEY_OWNER)
            )
            db.session.add(new_car)
            db.session.commit()
            
            return response(message=MSG_CAR_ADDED, status_code=201)
        
        except Exception:
            db.session.rollback()
            return response(message=ERR_CAR_EXISTS, status_code=400)


@ns.route("/cars/<string:car_license_plate>")
class CarDetail(Resource):
    def get(self, car_license_plate):
        try:
            car = Car.query.filter_by(license_plate=car_license_plate).first()
            check_object_exists(car, KEY_CAR.format(car_license_plate))
            data = {
                KEY_LICENSE_PLATE: car.license_plate,
                KEY_BRAND: car.brand,
                KEY_MODEL: car.model,
                KEY_OWNER: car.owner
            }

            return response(data=data, status_code=200)
        except ObjectNotFound as e:
            return response(message=str(e), status_code=e.status_code)
    
    
    @ns.expect(get_car_model(ns))
    def put(self, car_license_plate):
        data = request.get_json()
        
        car = Car.query.get_or_404(car_license_plate)
        car.license_plate = data.get(KEY_LICENSE_PLATE, car.license_plate)
        car.brand = data.get(KEY_BRAND, car.brand)
        car.model = data.get(KEY_MODEL, car.model)
        car.owner = data.get(KEY_OWNER, car.owner)
        
        db.session.commit()
        
        return response(message=MSG_CAR_UPDATED, status_code=200)


@ns.route("/spots")
class ParkingSpots(Resource):
    def get(self):
        spots = ParkingSpot.query.all()
        data = [{KEY_NUMBER: spot.number, KEY_IS_OCCUPIED: spot.is_occupied} for spot in spots]
        return response(data=data, status_code=200)

    @ns.expect(get_parking_spot_model(ns))
    def post(self):
        try:
            data = request.get_json()
            new_spot = ParkingSpot(
                number=data.get(KEY_NUMBER),
                is_occupied=data.get(KEY_IS_OCCUPIED, False)
            )
            
            db.session.add(new_spot)
            db.session.commit()
            
            return response(message=MSG_SPOT_ADDED, status_code=201)
        except Exception:
            db.session.rollback()
            return response(message=ERR_SPOT_OCCUPIED, status_code=400)


@ns.route("/spots/<int:spot_number>")
class ParkingSpotDetail(Resource):
    def get(self, spot_number):
        try:
            spot = ParkingSpot.query.filter_by(number=spot_number).first()
            check_object_exists(spot, KEY_SPOT.format(spot_number))
            data = {
                KEY_NUMBER: spot.number,
                KEY_IS_OCCUPIED: spot.is_occupied
            }
            return response(data=data, status_code=200)
        except ObjectNotFound as e:
            return response(message=str(e), status_code=e.status_code)

    @ns.expect(get_parking_spot_model(ns))
    def put(self, spot_number):
        data = request.get_json()
        
        spot = ParkingSpot.query.get_or_404(spot_number)
        spot.number = data.get(KEY_NUMBER, spot.number)
        spot.is_occupied = data.get(KEY_IS_OCCUPIED, spot.is_occupied)
        
        db.session.commit()
        
        return response(message=MSG_SPOT_UPDATED, status_code=200)


@ns.route("/sessions")
class ParkingSessions(Resource):
    def get(self):
        sessions = ParkingSession.query.all()
        data = [{KEY_CAR_LICENSE_PLATE: session.car_license_plate, KEY_SPOT_NUMBER: session.spot_number, KEY_ID: session.id, KEY_CHECK_IN: session.check_in_time, KEY_CHECK_OUT: session.check_out_time, KEY_COST: session.cost}
            for session in sessions]
        
        return response(data=data, status_code=200)


@ns.route("/sessions/<int:session_id>")
class ParkingSessionDetail(Resource):
    def get(self, session_id):
        try:
            session = ParkingSession.query.get(session_id)
            check_object_exists(session, KEY_SESSION)
            data = {
                KEY_CAR_LICENSE_PLATE: session.car_license_plate,
                KEY_SPOT_NUMBER: session.spot_number,
                KEY_CHECK_IN: session.check_in_time,
                KEY_CHECK_OUT: session.check_out_time,
                KEY_COST: session.cost
            }
            
            return response(data=data, status_code=200)
        except ObjectNotFound as e:
            return response(message=str(e), status_code=e.status_code)


@ns.route("/sessions/check-in")
class SessionsCheckIn(Resource):
    @ns.expect(get_session_model(ns))
    def post(self):
        try:
            data = request.get_json()
            number=data.get(KEY_SPOT_NUMBER)
            spot = ParkingSpot.query.filter_by(number=number).first()
            
            check_object_exists(spot, KEY_SPOT.format(number))
            check_is_spot_occupied(spot)

            new_session = ParkingSession(
                car_license_plate=data.get(KEY_CAR_LICENSE_PLATE),
                spot_number=data.get(KEY_SPOT_NUMBER),
                check_in_time=data.get(KEY_CHECK_IN),
                check_out_time=None,
            )
            spot.is_occupied = True

            db.session.add(new_session)
            db.session.commit()
            
            response_data = {KEY_SESSION_ID: new_session.id}
            return response(message=MSG_SESSION_STARTED, data=response_data, status_code=201)
        except ObjectNotFound as e:
            return response(message=str(e), status_code=e.status_code)
        except SpotAlreadyOccupied as e:
            return response(message=str(e), status_code=e.status_code)


@ns.route("/sessions/check-out/<string:car_license_plate>")
class SessionsCheckOut(Resource):
    def post(self, car_license_plate):
        try:
            session = ParkingSession.query.filter_by(car_license_plate=car_license_plate).first()
            
            check_object_exists(session, KEY_SESSION.format(car_license_plate))
            check_session_status(session)

            session.check_out_time = datetime.now()
            session.cost, hours = calculate_cost(session.check_in_time, session.check_out_time)

            session.spot.is_occupied = False
            db.session.commit()
            
            response_data = {
                KEY_DURATION_HOURS: hours,
                KEY_COST: session.cost
            }
            return response(message=MSG_CHECKED_OUT_SUCCESS, data=response_data, status_code=200)
        
        except ObjectNotFound as e:
            return response(message=str(e), status_code=e.status_code)
        except SessionAlreadyCheckedOut as e:
            return response(message=str(e), status_code=e.status_code)