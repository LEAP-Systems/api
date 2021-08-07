from flask_restx import Namespace
from app.v1.models.threshold import Threshold


# define namespaces
api = Namespace('threshold', description='threshold parameters')
threshold_model = api.model('Threshold', Threshold.api_model())
