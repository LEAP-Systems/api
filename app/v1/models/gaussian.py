from typing import Any, Dict
import mongoengine as me
from flask_restx import fields


class GaussianCurve(me.EmbeddedDocument):
    amplitude = me.FloatField()
    sigma_x = me.FloatField()
    sigma_y = me.FloatField()
    mu_x = me.IntField()
    mu_y = me.IntField()

    @staticmethod
    def api_model() -> Dict[str, Any]:
        return {
            'amplitude': fields.Float(required=True, description="peak amplitude"),
            'sigma_x': fields.Float(required=True, description="standard deviation (σ) in x"),
            'sigma_y': fields.Float(required=True, description="standard deviation (σ) in y"),
            'mu_x': fields.Integer(required=True, description="mean (μ) in x"),
            'mu_y': fields.Integer(required=True, description="mean (μ) in y"),
        }
