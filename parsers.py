import werkzeug
from flask_restx import reqparse

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, 
                           location='files', help="Image you want to upload", required=True)

getimage_parser = reqparse.RequestParser()
getimage_parser.add_argument('uuid', type=str, required=True, help='id of the image', location='args')