import mongoengine as me
from datetime import datetime
from flask_restx import fields
from typing import Any, Dict


class Capture(me.Document):

    path = me.StringField()
    created_at = me.DateTimeField(required=True)
    updated_at = me.DateTimeField(required=True, default=datetime.now())

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    @staticmethod
    def commit(): ...

    @staticmethod
    def post_model() -> Dict[str, Any]:
        return {
            'data': fields.String(required=True, description="Base64 encoded capture data"),
            'algorithm': fields.String(
                required=True,
                description="Algorithm selection: sector | gauss | all"
            )
        }
