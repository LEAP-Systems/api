# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields, Namespace

api = Namespace('gaussian blur', description='gaussian blur parameters')
gaussian_blur_request_schema = {
    'type': 'object',
    'properties': {
        'kernel_width': {
            'type': 'integer',
            'minimum': 1,
            'example': 5,
            'not': {'multipleOf': 2}
        },
        'kernel_height': {
            'type': 'integer',
            'minimum': 1,
            'example': 5,
            'not': {'multipleOf': 2}
        },
    },
    'required': [
        'kernel_width',
        'kernel_height'
    ],
}

gaussian_blur_model = api.model(
    'Gaussian Blur',
    {
        'kernel_width': fields.Integer(required=True, min=1, description="kernel width"),
        'kernel_height': fields.Integer(required=True, min=1, description="kernel height"),
    }
)


class GaussianBlur(me.EmbeddedDocument):

    # kernel shape must be odd numbers
    kernel_width = me.IntField(required=True, min_value=1)
    kernel_height = me.IntField(required=True, min_value=1)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))
