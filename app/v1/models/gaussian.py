from typing import Any, Dict
import mongoengine as me
from flask_restx import fields, Namespace
from flask_restx import Namespace

api = Namespace('gaussian curve', description='gaussian curve parameters')
model = api.model(
    'Gaussian Curve',
    {
        'amplitude': fields.Float(required=True, min=0, max=255, description="peak amplitude"),
        'sigma_x': fields.Float(required=True, min=0, description="standard deviation (σ) in x"),
        'sigma_y': fields.Float(required=True, min=0, description="standard deviation (σ) in y"),
        'mu_x': fields.Integer(required=True, min=0, description="mean (μ) in x"),
        'mu_y': fields.Integer(required=True, min=0, description="mean (μ) in y"),
    }
)
class GaussianCurve(me.EmbeddedDocument):

    amplitude = me.FloatField(required=True, min_value=0, max_value=255)
    sigma_x = me.FloatField(required=True, min_value=0)
    sigma_y = me.FloatField(required=True, min_value=0)
    mu_x = me.IntField(required=True, min_value=0)
    mu_y = me.IntField(required=True, min_value=0)
