from flask_restx import Namespace
from app.v1.models.capture import Capture

# define namespaces
api = Namespace('capture', description='Endpoint for uploading and deleting raw captures')
post_model = Capture.post_model(api.parser())
capture_model = api.model('Capture', Capture.api_model())
