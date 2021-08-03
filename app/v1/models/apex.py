# -*- coding: utf-8 -*-
import mongoengine as me
from app.v1.models.gauss import GaussCurve


class Apex(me.EmbeddedDocument):
    initial = me.EmbeddedDocumentField(GaussCurve)
    optimized = me.EmbeddedDocumentField(GaussCurve)
