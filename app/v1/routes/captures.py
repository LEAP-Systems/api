# -*- coding: utf-8 -*-
import uuid
from flask import current_app as app
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from mongoengine.errors import ValidationError
from app import db
from app.v1.models.captures import Capture, CaptureModel


# define namespaces
api = Namespace('capture', description='CRUD endpoint for captures')
post_model = Capture.post_model(api.parser())


@api.route('')
class Captures(Resource):
    def get(self):
        return make_response(jsonify(Capture.objects().to_json()), 200)  # type: ignore

    @api.expect(post_model, validate=True)
    def post(self):
        # process payload args
        args = post_model.parse_args(strict=True)
        app.logger.debug("args: %s", args)
        model = CaptureModel(args)
        algorithm = model.algorithm
        img = model.file
        app.logger.debug("Received upload: %s", img)
        app.logger.debug("Running processing with algorithm: %s", algorithm)
        # save png to disk (uuid for file collision avoidance)
        img_path = "{}/{}.png".format(app.config.get("STORAGE_PATH"), uuid.uuid4().hex)
        app.logger.debug("Constucted image path: %s", img_path)
        img.save(img_path)
        app.logger.info("Successfully wrote capture to file system as %s", img_path)
        capture = Capture(path=img_path)
        try:
            capture.save()
        except ValidationError as exc:
            app.logger.exception("Capture validation failed: %s", exc)
            return make_response(jsonify(message="Invalid types for models {}".format(exc))), 400
        # kickstart async processing request
        return make_response(jsonify(capture), 202)

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204
