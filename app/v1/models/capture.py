# -*- coding: utf-8 -*-
"""
Capture Models
===============
Modified: 2021-07

Copyright © 2021 LEAP. All Rights Reserved.
"""

import mongoengine as me
from datetime import datetime
from flask_restx import fields, Namespace
from werkzeug.datastructures import FileStorage

api = Namespace('capture', description='Endpoint for uploading and deleting raw captures')
post_model = api.parser()
post_model.add_argument(
    "file",
    type=FileStorage,
    location='files',
    help="Capture for processing"
)
model = api.model(
    'Capture', 
    {
        'id': fields.String(required=True, description="capture id"),
        'path': fields.String(required=True, description="path to server-side image"),
        'created_at': fields.String(required=True, description="Time of upload"),
    }
)

class Capture(me.Document):

    path = me.StringField(unique=True)
    created_at = me.StringField(required=True)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, vars(self))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        return super().save(*args, **kwargs)
