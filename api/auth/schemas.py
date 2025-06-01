from flask_restx import fields


def get_userid_model(api):
    return api.model(
        "UserID",
        {
            "id": fields.String(required=True, description="User ID"),
        },
    )

