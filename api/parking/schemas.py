from flask_restx import fields


def get_car_model(api):
    return api.model(
        "Car",
        {
            "license_plate": fields.String(),
            "brand": fields.String(),
            "model": fields.String(),
            "owner": fields.String(),
        },
    )


def get_parking_spot_model(api):
    return api.model(
        "ParkingSpot",
        {
            "number": fields.Integer(),
            "is_occupied": fields.Boolean(),
        },
    )


def get_session_model(api):
    return api.model(
        "ParkingSession",
        {
            "car_license_plate": fields.String(),
            "spot_number": fields.Integer(),
        },
    )
