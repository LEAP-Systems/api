from flask_restx import Namespace
from app.v1.models.dialation import Dialation


# define namespaces
api = Namespace('dialation', description='Image dialation')
dialation_model = api.model('Dialation', Dialation.api_model())
