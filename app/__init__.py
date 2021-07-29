# -*- coding: utf-8 -*-
from flask import Flask
from flask_restx import Api
from flask.blueprints import Blueprint
from flask_mongoengine import MongoEngine


# Globally accessible libraries
db = MongoEngine()


def init_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    bp = Blueprint("api", __name__, url_prefix="/v1")
    api = Api(
        bp,
        version="1.0",
        title="LEAP Systems API",
        description="Image Processing Backend",
        contact_email="christian@leapsystems.online"
    )
    # Initialize Plugins
    db.init_app(app)
    with app.app_context():
        # Include our Routes
        from app.v1.routes.captures import api as captures
        app.register_blueprint(bp)
        # add resource endpoints
        api.add_namespace(captures)
        return app
