# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields, Namespace
from enum import Enum

api = Namespace('threshold', description='threshold parameters')


class ThresholdTypes(Enum):
    INVERSE = 'inverse'
    NORMAL = 'normal'


threshold_request_schema = {
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
            'enum': ['normal', 'inverse']
        },
    },
    'required': [
        'threshold',
        'output',
        'type'
    ],
    'additionalProperties': False
}
threshold_post_model = api.schema_model('threshold_post_request', threshold_request_schema)

threshold_model = api.model(
    'Threshold',
    {
        'type': fields.String(required=True, description="thresholding type (inverse, normal)"),
        'output': fields.Integer(required=True, min=0, max=255, description="erosion iterations"),
        'threshold': fields.Integer(required=True, min=0, max=255, description="threshold value"),
    }
)


class Threshold(me.EmbeddedDocument):

    threshold = me.IntField(required=True, min_value=0, max_value=255)
    output = me.IntField(required=True, min_value=0, max_value=255)
    type = me.EnumField(ThresholdTypes, default=ThresholdTypes.NORMAL, required=True)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))
