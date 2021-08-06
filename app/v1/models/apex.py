# -*- coding: utf-8 -*-
from typing import Any, Dict
from flask_restx import fields
import mongoengine as me
from app.v1.namespaces.gaussian import gaussian_model
from app.v1.models.gaussian import GaussianCurve


class Apex(me.EmbeddedDocument):
    initial = me.EmbeddedDocumentField(GaussianCurve)
    optimized = me.EmbeddedDocumentField(GaussianCurve)
    chi = me.FloatField()

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
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
