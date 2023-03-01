import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config  # not worked without dot

db = SQLAlchemy()


def create_app(config_name):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .modules import clients
    from .modules import parkings
    from .modules import client_parkings
    from .modules import error_handlers

    app.register_blueprint(clients.bp)
    app.register_blueprint(parkings.bp)
    app.register_blueprint(client_parkings.bp)
    app.register_blueprint(error_handlers.bp)

    return app
