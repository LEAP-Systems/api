# -*- coding: utf-8 -*-
"""
Captures Routes
===============
Modified: 2021-07

Copyright © 2021 LEAP. All Rights Reserved.
"""

import os
import uuid

from flask import current_app as app
from flask import request, jsonify, make_response
from flask_restx import Resource
from mongoengine.errors import ValidationError
from werkzeug.datastructures import FileStorage
from app.v1.models.threshold import Threshold, api, model, threshold_post_model


@api.route('')
class ThresholdList(Resource):

    @api.marshal_with(model, as_list=True, code=200)
    def get(self):
        """
        Get list of captures
        """
        threshold_list = Threshold.objects()  # type: ignore
        return list(threshold_list)

    @api.route('/<string:capture_id>')
    @api.marshal_with(model, code=201)
    @api.expect(threshold_post_model, validate=True)
    def post(self, capture_id: str):
        """
        Apply new thresholding to a target image
        """
        # process payload args
        payload: dict = request.get_json()
        app.logger.info("Received Payload: %s", payload)
        app.logger.debug("Received upload: %s", img)
        # save png to disk (uuid for file collision avoidance)
        img_path = "{}/{}.png".format(app.config.get("STORAGE_PATH"), uuid.uuid4().hex)
        app.logger.debug("Constucted image path: %s", img_path)
        img.save(img_path)
        app.logger.info("Successfully wrote capture to file system as %s", img_path)
        capture = Threshold(
            path=img_path
        )
        try:
            capture.save()
        except ValidationError as exc:
            app.logger.exception("Capture validation failed: %s", exc)
            return make_response(jsonify(message="Invalid types for models {}".format(exc))), 400
        return capture


@api.route('/<string:id>')
class Thresholds(Resource):

    @api.marshal_with(model, code=200)
    def get(self, id: str):
        """
        Get a single threshold
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
