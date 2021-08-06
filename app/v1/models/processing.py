# -*- coding: utf-8 -*-
import mongoengine as me
from datetime import datetime
from typing import Any, Dict
from flask_restx import fields


class GaussianBlur(me.EmbeddedDocument):
    kernel_width = me.IntField(required=True)
    kernel_height = me.IntField(required=True)


class Erosion(me.Document):

    iterations = me.IntField(required=True, min_value=1)
    # kernel shape must be odd numbers
    kernel_width = me.IntField(required=True, min_value=1)
    kernel_height = me.IntField(required=True, min_value=1)
    created_at = me.StringField(required=True)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'id': fields.String(required=True, description="capture id"),
            'iterations': fields.Integer(required=True, min=1, description="erosion iterations"),
            'kernel_width': fields.Integer(required=True, min=1, description="kernel width"),
            'kernel_height': fields.Integer(required=True, min=1, description="kernel height"),
            'created_at': fields.String(required=True, description="Time of upload"),
        }

class Dialation(me.EmbeddedDocument):
    kernel_width = me.IntField(required=True)
    kernel_height = me.IntField(required=True)
    iterations = me.IntField(required=True)


class Threshold(me.EmbeddedDocument):
    threshold = me.IntField(required=True)
    output = me.IntField(required=True)
    type = me.StringField(required=True)
