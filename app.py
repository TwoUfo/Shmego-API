from flask import Flask
from flask_migrate import Migrate

from api import blueprint, db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blueprint)
    db.init_app(app)

    migrate = Migrate(app, db)

    return app
