# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx.reqparse import RequestParser
from flask_restx import fields, Namespace
from datetime import datetime

from app.v1.models.capture import Capture
from app.v1.models.apex import Apex
from app.v1.models.apex import model as apex_model
from app.v1.models.dialation import Dialation
from app.v1.models.dialation import model as dialation_model
from app.v1.models.threshold import Threshold
from app.v1.models.threshold import model as threshold_model
from app.v1.models.erosion import Erosion
from app.v1.models.erosion import model as erosion_model
from app.v1.models.gaussian_blur import GaussianBlur
from app.v1.models.gaussian_blur import model as gaussian_blur_model


api = Namespace('model', description='gaussian curve fitting models')
post_model = api.parser()
post_model.add_argument(
    "capture_id",
    type=str,
    location='json',
    help="Capture id for processing"
)
post_model.add_argument(
    "iterations",
    type=int,
    location='json',
    help="Minimization iterations"
)
post_model.add_argument(
    "divisor",
    type=int,
    location='json',
    help="Resolution divisor"
)

model = api.model(
    'Model',
    {
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
)

class Model(me.Document):
    capture_id = me.ReferenceField(Capture, required=True)
    created_at = me.StringField(required=True)
    gaussian_blur = me.ReferenceField(GaussianBlur)
    erosion = me.ReferenceField(Erosion)
    dialation = me.ReferenceField(Dialation)
    threshold = me.ReferenceField(Threshold)
    elapsed = me.FloatField(required=True)
    apexes = me.EmbeddedDocumentListField(Apex)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)
