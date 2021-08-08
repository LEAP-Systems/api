# -*- coding: utf-8 -*-
import mongoengine as me
from flask_restx import fields, Namespace
from app.v1.models.gaussian import GaussianCurve
from app.v1.models.gaussian import model as gaussian_model


api = Namespace('apex', description='apex')
model = api.model(
    'Apex', 
    {
        'chi': fields.Float(description="chi squared error (χ2)"),
        'initial': fields.Nested(
            gaussian_model,
            description="Initial gaussian parameters",
            required=True
        ),
        'optimized': fields.Nested(
            gaussian_model,
            description="Optimized gaussian parameters",
            required=True
        ),
    }
)

class Apex(me.EmbeddedDocument):
    initial = me.EmbeddedDocumentField(GaussianCurve)
    optimized = me.EmbeddedDocumentField(GaussianCurve)
    chi = me.FloatField()

