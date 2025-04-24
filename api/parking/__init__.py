from flask_restx import Namespace

ns = Namespace("parking")

from api.parking import routes
