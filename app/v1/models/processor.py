# -*- coding: utf-8 -*-
"""
Image Processor
===============
Modified: 2021-08

Copyright © 2021 LEAP. All Rights Reserved.
"""
import mongoengine as me
from flask_restx import fields, Namespace
from datetime import datetime

from app.v1.models.dialation import Dialation, dialation_request_schema, dialation_model
from app.v1.models.threshold import Threshold, threshold_request_schema, threshold_model
from app.v1.models.erosion import Erosion, erosion_request_schema, erosion_model
from app.v1.models.gaussian_blur import (
    GaussianBlur, gaussian_blur_request_schema, gaussian_blur_model
)

api = Namespace('processor', description='image processing specifications')
processor_request_schema = {
    'type': 'object',
    'properties': {
        'gaussian_blur': gaussian_blur_request_schema,
        'dialation': dialation_request_schema,
        'erosion': erosion_request_schema,
        'threshold': threshold_request_schema
    },
    'additionalProperties': False
}


processor_post_model = api.schema_model('post_request', processor_request_schema)

processor_model = api.model(
    'Processor',
    {
        'id': fields.String(required=True, description="processor id"),
        'created_at': fields.String(required=True, description="processor creation timestamp"),
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
    }
)


class Processor(me.Document):
    created_at = me.StringField(required=True)
    gaussian_blur = me.EmbeddedDocumentField(GaussianBlur)
    erosion = me.EmbeddedDocumentField(Erosion)
    dialation = me.EmbeddedDocumentField(Dialation)
    threshold = me.EmbeddedDocumentField(Threshold)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)
