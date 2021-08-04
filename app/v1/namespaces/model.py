from flask_restx import Namespace
from app.v1.models.model import Model

# define namespaces
api = Namespace('model', description='gaussian curve fitting models')
post_model = Model.post_model(api.parser())
model_model = api.model('Model', Model.api_model())
