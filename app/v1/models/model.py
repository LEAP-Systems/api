# -*- coding: utf-8 -*-
import mongoengine as me
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
request_schema = {
    'type': 'object',
    'properties': {
        'capture_id': {
            'type': 'string',
            "minLength": 24,
            "maxLength": 24
        },
        'iterations': {
            'type': 'integer',
            'minimum': 1
        },
        'divisor': {
            'type': 'integer',
            'minimum': 1
        },
        'gaussian_blur': {
            'type': 'object',
            'properties': {
                'kernel_width': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
                'kernel_height': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
            },
            'required': [
                'kernel_width',
                'kernel_height'
            ],
        },
        'dialation': {
            'type': 'object',
            'properties': {
                'iterations': {
                    'type': 'integer',
                    'minimum': 1
                },
                'kernel_width': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
                'kernel_height': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
            },
            'required': [
                'kernel_width',
                'kernel_height',
                'iterations'
            ],
        },
        'erosion': {
            'type': 'object',
            'properties': {
                'iterations': {
                    'type': 'integer',
                    'minimum': 1
                },
                'kernel_width': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
                'kernel_height': {
                    'type': 'integer',
                    'minimum': 1,
                    'not': {'multipleOf': 2}
                },
            },
            'required': [
                'kernel_width',
                'kernel_height',
                'iterations'
            ],
        },
        'threshold': {
            'type': 'object',
            'properties': {
                'threshold': {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 255
                },
                'output': {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': 255
                },
                'type': {
                    'type': 'string',
                    'enum': ["normal", "inverse"]
                },
            },
            'required': [
                'threshold',
                'output',
                'type'
            ],
        }
    },
    'required': [
        'capture_id',
        'iterations',
        'divisor'
    ],
    'additionalProperties': False
}
post_model = api.schema_model('post_request', request_schema)


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
