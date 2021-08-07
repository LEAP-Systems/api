from flask_restx import Namespace
from app.v1.models.erosion import Erosion


# define namespaces
api = Namespace('erosion', description='Image erosion')
erosion_model = api.model('Erosion', Erosion.api_model())
