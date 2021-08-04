# -*- coding: utf-8 -*-
import mongoengine as me
from app.v1.models.apex import Apex
from typing import Any, Dict
from flask_restx.reqparse import RequestParser
from flask_restx import fields
from app.v1.models.capture import Capture
from app.v1.namespaces.apex import apex_model
from app.v1.models.processing import Dialation, Erosion, GaussianBlur, Threshold


class Model(me.Document):
    capture_id = me.ReferenceField(Capture, required=True)
    created_at = me.StringField(required=True)
    gaussian_blur = me.EmbeddedDocumentField(GaussianBlur)
    erosions = me.EmbeddedDocumentField(Erosion)
    dialations = me.EmbeddedDocumentField(Dialation)
    threshold = me.EmbeddedDocumentField(Threshold)
    elapsed = me.FloatField(required=True)
    chi_squared_error = me.FloatField(required=True)
    apexes = me.EmbeddedDocumentListField(Apex)

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'id': fields.String(required=True, description="model id"),
            'capture_id': fields.String(required=True, description="capture id"),
            'created_at': fields.String(required=True, description="model creation timestamp"),
            'chi_squared_error': fields.Float(required=True, description="chi squared error"),
            'elapsed': fields.Float(required=True, description="curve fitting elapsed time"),
            'apexes': fields.List(
                fields.Nested(
                    apex_model,
                    description="Apex solution",
                    required=True
                )
            )
        }

    @staticmethod
    def post_model(model: RequestParser) -> RequestParser:
        model.add_argument(
            "capture_id",
            type=str,
            location='body',
            help="Capture id for processing"
        )
        model.add_argument(
            "iterations",
            type=int,
            location='body',
            help="Minimization iterations"
        )
        model.add_argument(
            "divisor",
            type=int,
            location='body',
            help="Resolution divisor"
        )
        return model
