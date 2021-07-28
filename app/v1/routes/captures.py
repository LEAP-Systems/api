# -*- coding: utf-8 -*-
import base64
from flask import current_app as app
from flask_restx import Namespace, Resource
from app import db
from app.v1.models.captures import Capture

# define namespace
api = Namespace('images', description='CRUD endpoint for images')
image_schema = api.model('Captures', Capture.api_model())


class Image(Resource):
    def get(self, id: int): ...

    @api.expect(image_schema, validate=True)
    def post(self):
        img = args["data"]
        ib = base64.b64decode(img)
        with open('samples/server.png', 'wb') as open_file:
            open_file.write(ib)
        app.logger.info("wrote image to fs")
        return "Created", 201

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204
