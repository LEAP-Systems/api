# -*- coding: utf-8 -*-
import base64
import uuid
from flask import current_app as app
from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource
from app.v1.models.captures import Capture

# define namespace
api = Namespace('captures', description='CRUD endpoint for captures')
image_schema = api.model('Capture', Capture.post_model())


@api.route('')
class Captures(Resource):
    def get(self, id: int): ...

    @api.expect(image_schema, validate=True)
    def post(self):
        payload: dict = request.get_json()
        # process payload args
        app.logger.info("Received payload: %s", payload)
        img = payload.get("data")
        # decode raw image data
        ib = base64.b64decode(img)
        # save png to disk (uuid for file collision avoidance)
        img_path = "{}/{}.png".format(app.config.get("STORAGE_PATH"), uuid.uuid4().hex)
        with open(img_path, 'wb') as open_file:
            open_file.write(ib)
        app.logger.info("Successfully wrote capture to file system as %s", img_path)
        # write capture resource to mongo

        # kickstart async processing request
        return make_response(jsonify(message="Accepted"), 202)

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204
