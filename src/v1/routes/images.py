import base64
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

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
        app.logger.info("wrote image to fs")
        return "Created", 201

    def put(self, id: int): ...

    def delete(self, id: int):
        return '', 204
