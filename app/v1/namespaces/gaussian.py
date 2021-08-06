from flask_restx import Namespace
from app.v1.models.gaussian import GaussianCurve


# define namespaces
api = Namespace('gaussian', description='Gaussian curve parameters')
gaussian_model = api.model('GaussianCurve', GaussianCurve.api_model())
