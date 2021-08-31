# -*- coding: utf-8 -*-
"""
Processor Routes
================
Modified: 2021-08

Copyright © 2021 LEAP. All Rights Reserved.
"""

from flask import request
from flask import current_app as app
from flask_restx import Resource
from app.v1.models.processor import Processor, api, processor_model, processor_post_model


@api.route('')
class ProcessorList(Resource):

    @api.marshal_with(processor_model, as_list=True, code=200)
    def get(self) -> list:
        """
        Get list of captures
        """
        procesor_list = Processor.objects()  # type: ignore
        return list(procesor_list)

    @api.expect(processor_post_model, validate=True)
    @api.marshal_with(processor_model, code=200)
    def post(self):
        payload: dict = request.get_json()
        app.logger.info("Received Payload: %s", payload)


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
        Delete a single capture
        """
        Processor.objects.get(id=id).delete()  # type: ignore
        return '', 204
