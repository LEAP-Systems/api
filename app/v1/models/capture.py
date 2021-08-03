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


class Capture(me.Document):

    path = me.StringField(unique=True)
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
            'path': fields.String(required=True, description="path to server-side image"),
            'created_at': fields.String(required=True, description="Time of upload"),
        }

    @staticmethod
    def post_model(model: RequestParser) -> RequestParser:
        model.add_argument(
            "file",
            type=FileStorage,
            location='files',
            help="Capture for processing"
        )
        return model
