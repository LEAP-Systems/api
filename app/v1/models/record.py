# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields, Namespace
from datetime import datetime

from app.v1.models.apex import Apex
from app.v1.models.apex import model as apex_model
from app.v1.models.capture import Capture
from app.v1.models.processor import Processor

api = Namespace('record', description='Imaging records')
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
        'required': [
            'capture_id',
            'iterations',
            'divisor'
        ],
        'additionalProperties': False
    }
}
post_model = api.schema_model('Record', request_schema)


model = api.model(
    'Record',
    {
        'id': fields.String(required=True, description="model id"),
        'capture_id': fields.String(required=True, description="capture"),
        'processor_id': fields.String(required=False, description="image processor"),
        'created_at': fields.String(required=True, description="model creation timestamp"),
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


class Record(me.Document):
    capture_id = me.ReferenceField(Capture, required=True)
    processor_id = me.ReferenceField(Processor, required=False)
    created_at = me.StringField(required=True)
    elapsed = me.FloatField(required=True)
    apexes = me.EmbeddedDocumentListField(Apex)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)
