# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from app.v1.routes.users import Users


# Globally accessible libraries
db = MongoEngine()
api = Api()


def init_app():
    """Initialize the core application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # Initialize Plugins
    api.init_app(app)
    db.init_app(app)
    with app.app_context():
        # Include our Routes
        from app.v1.routes import captures
        # add resource endpoints
        api.add_resource(Users, '/users/<int:id>', '/users', endpoint='user')
        return app
