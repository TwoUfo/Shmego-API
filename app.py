from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from api import blueprint, db
from config import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blueprint)
    db.init_app(app)

    migrate = Migrate(app, db)
    
    origins = os.getenv('CORS_RESOURCES').split(',')
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)

    return app
