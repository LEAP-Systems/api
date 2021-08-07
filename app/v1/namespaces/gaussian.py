from flask_restx import Namespace
from app.v1.models.gaussian import GaussianCurve


# define namespaces
api = Namespace('gaussian curve', description='gaussian curve parameters')
gaussian_model = api.model('Gaussian Curve', GaussianCurve.api_model())
