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
