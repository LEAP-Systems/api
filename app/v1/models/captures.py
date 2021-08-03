# -*- coding: utf-8 -*-
"""
Capture Models
===============
Modified: 2021-07

Copyright © 2021 LEAP. All Rights Reserved.
"""

import mongoengine as me
from datetime import datetime
from typing import Any, Dict
from flask_restx import fields
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage


class CaptureModel:
    def __init__(self, model: Dict[str, Any]) -> None:
        self.algorithm: str = model["algorithm"]
        self.file: FileStorage = model["file"]


class Capture(me.Document):

    path = me.StringField(unique=True)
    created_at = me.StringField(required=True)
    updated_at = me.StringField(required=True, default=datetime.now().isoformat())

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'id': fields.String,
            'path': fields.String,
            'created_at': fields.String,
            'updated_at': fields.String
        }

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
