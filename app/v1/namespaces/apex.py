from flask_restx import Namespace
from app.v1.models.apex import Apex


# define namespaces
api = Namespace('apex', description='apex')
apex_model = api.model('Apex', Apex.api_model())
