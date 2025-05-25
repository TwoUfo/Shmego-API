import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from api import blueprint, db
from config import Config
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blueprint)
    db.init_app(app)

    migrate = Migrate(app, db)
    
    app.config["SESSION_SQLALCHEMY"] = db
    Session(app)

    origins = os.getenv("CORS_RESOURCES").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)

    return app
