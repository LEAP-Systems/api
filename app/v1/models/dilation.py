# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields, Namespace

api = Namespace('dilation', description='Image dilation')

dilation_request_schema = {
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
}

dilation_model = api.model(
    'dilation',
    {
        'iterations': fields.Integer(required=True, min=1, description="dilation iterations"),
        'kernel_width': fields.Integer(required=True, min=1, description="kernel width"),
        'kernel_height': fields.Integer(required=True, min=1, description="kernel height"),
    }
)


class dilation(me.EmbeddedDocument):

    iterations = me.IntField(required=True, min_value=1)
    # kernel shape must be odd numbers
    kernel_width = me.IntField(required=True, min_value=1)
    kernel_height = me.IntField(required=True, min_value=1)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))
