import mongoengine as me
from flask_restx import fields
from typing import Any, Dict


class Capture(me.Document):  # type: ignore
    id = me.IntField(required=True)
    path = me.StringField()
    data = me.StringField()

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'data': fields.String(required=True, description="raw capture data")
        }
