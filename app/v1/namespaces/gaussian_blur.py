
from flask_restx import Namespace
from app.v1.models.gaussian_blur import GaussianBlur

# define namespaces
api = Namespace('gaussian blur', description='gaussian blur parameters')
gaussian_blur_model = api.model('Gaussian Blur', GaussianBlur.api_model())
