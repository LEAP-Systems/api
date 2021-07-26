from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = ""
db = SQLAlchemy(app)

# resource_schema = {
#     'id': fields.Integer,
#     'data': fields.String
# }


@app.errorhandler(404)
def resource_not_found(err):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(err)), 404


images = {}


api.add_resource(Image, "/image", "/image/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
