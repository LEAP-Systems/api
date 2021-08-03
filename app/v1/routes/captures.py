# -*- coding: utf-8 -*-
import os
import uuid
from flask import current_app as app
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from mongoengine.errors import ValidationError
from app.v1.models.captures import Capture, CaptureModel


# define namespaces
api = Namespace('capture', description='CRUD endpoint for captures')
post_model = Capture.post_model(api.parser())
capture_marshal = api.model('Capture', Capture.api_model())


@api.route('')
class CapturesList(Resource):

    @api.marshal_with(capture_marshal, as_list=True, code=200)
    def get(self):
        """
        Get list of captures
        """
        captures_list = Capture.objects()  # type: ignore
        return list(captures_list)

    @api.marshal_with(capture_marshal, code=202)
    @api.expect(post_model, validate=True)
    def post(self):
        """
        Upload new image capture and asynchronously start processing execution
        """
        # process payload args
        args = post_model.parse_args(strict=True)
        app.logger.debug("args: %s", args)
        model = CaptureModel(args)
        algorithm = model.algorithm
        img = model.file
        app.logger.debug("Received upload: %s", img)
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
        app.logger.debug("Running processing with algorithm: %s", algorithm)
        # return response
        return capture


@api.route('/<string:id>')
class Captures(Resource):

    @api.marshal_with(capture_marshal, code=200)
    def get(self, id: str):
        """
        Get a single capture
        """
        capture = Capture.objects.get(id=id)  # type: ignore
        return capture

    def delete(self, id: str):
        """
        Delete a single capture
        """
        capture = Capture.objects.get(id=id)  # type: ignore
        os.remove(capture.path)
        capture.delete()
        return '', 204
