# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields
from typing import Any, Dict
from app.v1.models.gauss import GaussCurve

class Apex(me.EmbeddedDocument):
    initial = me.EmbeddedDocumentField(GaussCurve)
    optimized = me.EmbeddedDocumentField(GaussCurve)