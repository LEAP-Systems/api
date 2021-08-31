# -*- coding: utf-8 -*-
import os
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
    # create storage directory
    os.makedirs(app.config['STORAGE_PATH'], exist_ok=True)
    # Initialize Plugins
    db.init_app(app)
    with app.app_context():
        # Include our Routes
        from app.v1.routes.captures import api as captures
        from app.v1.routes.models import api as models
        from app.v1.routes.processor import api as processors
        # include models
        from app.v1.models.apex import api as apex
        from app.v1.models.gaussian import api as gaussian
        from app.v1.models.gaussian_blur import api as gaussian_blur
        from app.v1.models.erosion import api as erosion
        from app.v1.models.dialation import api as dialation
        from app.v1.models.threshold import api as threshold
        from app.v1.models.processor import api as processor
        app.register_blueprint(bp)
        # add resource endpoints
        api.add_namespace(captures)
        api.add_namespace(models)
        api.add_namespace(apex)
        api.add_namespace(gaussian)
        api.add_namespace(gaussian_blur)
        api.add_namespace(dialation)
        api.add_namespace(threshold)
        api.add_namespace(erosion)
        api.add_namespace(processor)
        api.add_namespace(processors)
        return app
