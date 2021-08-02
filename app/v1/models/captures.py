import mongoengine as me
from datetime import datetime
from typing import Any, Dict
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage


class CaptureModel:
    def __init__(self, model: Dict[str, Any]) -> None:
        self.algorithm: str = model["algorithm"]
        self.file: FileStorage = model["file"]


class Capture(me.Document):

    path = me.StringField(primary_key=True)
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
    def post_model(model: RequestParser) -> RequestParser:
        model.add_argument(
            "file",
            type=FileStorage,
            location='files',
            help="Capture for processing"
        )
        model.add_argument(
            "algorithm",
            type=str,
            choices=('sector', 'fit', 'all'),
            location='args',
            help="Algorithm"
        )
        return model
