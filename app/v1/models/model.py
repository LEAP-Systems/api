# -*- coding: utf-8 -*-
import mongoengine as me
from app.v1.models.apex import Apex
from typing import Any, Dict
from flask_restx.reqparse import RequestParser
from flask_restx import fields
from app.v1.models.capture import Capture
from app.v1.namespaces.apex import apex_model
from app.v1.namespaces.dialation import dialation_model
from app.v1.namespaces.threshold import threshold_model
from app.v1.namespaces.gaussian_blur import gaussian_blur_model
from app.v1.namespaces.erosion import erosion_model
from app.v1.models.dialation import Dialation
from app.v1.models.threshold import Threshold
from app.v1.models.erosion import Erosion
from app.v1.models.gaussian_blur import GaussianBlur

class Model(me.Document):
    capture_id = me.ReferenceField(Capture, required=True)
    created_at = me.StringField(required=True)
    gaussian_blur = me.ReferenceField(GaussianBlur)
    erosion = me.ReferenceField(Erosion)
    dialation = me.ReferenceField(Dialation)
    threshold = me.ReferenceField(Threshold)
    elapsed = me.FloatField(required=True)
    apexes = me.EmbeddedDocumentListField(Apex)

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'id': fields.String(required=True, description="model id"),
            'capture_id': fields.String(required=True, description="capture id"),
            'created_at': fields.String(required=True, description="model creation timestamp"),
            'erosion': fields.Nested(
                erosion_model,
                description="Erosion parameters"
            ),
            'dialation': fields.Nested(
                dialation_model,
                description="Dialation parameters"
            ),
            'threshold': fields.Nested(
                threshold_model,
                description="Thresholding parameters"
            ),
            'gaussian_blur': fields.Nested(
                gaussian_blur_model,
                description="Gaussian blur parameters"
            ),
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
            location='json',
            help="Capture id for processing"
        )
        model.add_argument(
            "iterations",
            type=int,
            location='json',
            help="Minimization iterations"
        )
        model.add_argument(
            "divisor",
            type=int,
            location='json',
            help="Resolution divisor"
        )
        return model
