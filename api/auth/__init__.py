from flask_restx import Namespace

ns = Namespace("auth")

from api.auth import routes
