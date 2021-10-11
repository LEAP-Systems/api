# -*- coding: utf-8 -*-
"""
Processor Routes
================
Modified: 2021-08

Copyright © 2021 LEAP. All Rights Reserved.
"""

from typing import Optional
from flask.helpers import make_response
from flask.json import jsonify

from mongoengine.errors import ValidationError
from app.logs.formatter import pformat
from app.v1.models.threshold import Threshold
from app.v1.models.dilation import Dilation
from app.v1.models.erosion import Erosion
from app.v1.models.gaussian_blur import GaussianBlur
from flask import request
from flask import current_app as app
from flask_restx import Resource
from app.v1.models.processor import Processor, api, processor_model, processor_post_model


@api.route('')
class ProcessorList(Resource):

    @api.marshal_with(processor_model, as_list=True, code=200)
    def get(self) -> list:
        """
        Get list of processors 
        """
        procesor_list = Processor.objects()  # type: ignore
        return list(procesor_list)

    @api.marshal_with(processor_model, code=200)
    @api.expect(processor_post_model, validate=True)
    def post(self):
        """
        Post new processor
        """
        payload: dict = request.get_json()
        app.logger.info("Received Payload: %s", pformat(payload))
        # extract optional parameters if any
        gaussian_blur_params: Optional[dict] = payload.get("gaussian_blur")
        erosion_params: Optional[dict] = payload.get("erosion")
        dilation_params: Optional[dict] = payload.get("dilation")
        threshold_params: Optional[dict] = payload.get("threshold")
        if gaussian_blur_params:
            gaussian_blur = GaussianBlur(
                kernel_width=gaussian_blur_params.get('kernel_width'),
                kernel_height=gaussian_blur_params.get('kernel_height')
            )
            payload["gaussian_blur"] = gaussian_blur
            app.logger.debug("Saved gaussian blur modifier: %s", gaussian_blur)
        if erosion_params:
            erosion = Erosion(
                kernel_width=erosion_params.get('kernel_width'),
                kernel_height=erosion_params.get('kernel_height'),
                iterations=erosion_params.get('iterations')
            )
            payload["erosion"] = erosion
            app.logger.debug("Saved erosion modifier: %s", erosion)
        if dilation_params:
            dilation = Dilation(
                kernel_width=dilation_params.get('kernel_width'),
                kernel_height=dilation_params.get('kernel_height'),
                iterations=dilation_params.get('iterations')
            )
            payload["dilation"] = dilation
            app.logger.debug("Saved dilation modifier: %s", dilation)
        if threshold_params:
            threshold = Threshold(
                threshold=threshold_params.get('threshold'),
                output=threshold_params.get('output'),
                type=threshold_params.get('type')
            )
            payload["threshold"] = threshold
            app.logger.debug("Saved threshold modifier: %s", threshold)
        processor = Processor(**payload)
        try:
            processor.save()
        except ValidationError as exc:
            app.logger.exception("Processor validation failed: %s", exc)
            return make_response(
                jsonify(message="Invalid types for processors {}".format(exc))
            ), 400
        app.logger.debug("Saved processor")
        return processor


@api.route('/<string:id>')
class Processors(Resource):

    @api.marshal_with(processor_model, code=200)
    def get(self, id: str):
        """
        Get a single processor 
        """
        processor = Processor.objects.get(id=id)  # type: ignore
        return processor

    def delete(self, id: str):
        """
        Delete a single processor
        """
        Processor.objects.get(id=id).delete()  # type: ignore
        return '', 204
