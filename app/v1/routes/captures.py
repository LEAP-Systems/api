# -*- coding: utf-8 -*-
import uuid
from flask import current_app as app
from flask import jsonify, make_response
from flask_restx import Namespace, Resource
from app.v1.models.captures import Capture, CaptureModel


# define namespaces
api = Namespace('captures', description='CRUD endpoint for captures')
post_model = Capture.post_model(api.parser())

@api.route('')
class Captures(Resource):
    def get(self, id: int): ...

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
        # write capture resource to mongo
        document = {
            'path': img_path
        }
        capture = Capture(**document).save()
        # kickstart async processing request
        return make_response(jsonify(capture), 202)

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204
