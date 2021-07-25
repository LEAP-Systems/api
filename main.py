import base64
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

images = {}

image_schema = reqparse.RequestParser()
image_schema.add_argument("data", type=str, help="Image data in bytes is required", required=True)


class Image(Resource):
    def get(self, id: int): ...

    def post(self):
        args = image_schema.parse_args(strict=True)
        img = args["data"]
        ib = base64.b64decode(img)
        with open('samples/server.png', 'wb') as open_file:
            open_file.write(ib)
        print(images)

        return "Created", 201

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204


api.add_resource(Image, "/image", "/image/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
