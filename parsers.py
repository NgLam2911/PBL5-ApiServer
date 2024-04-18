import werkzeug
from flask_restx import reqparse

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=werkzeug.datastructures.FileStorage, 
                           location='files', help="Image you want to upload", required=True)

getimage_parser = reqparse.RequestParser()
getimage_parser.add_argument('uuid', type=str, required=True, help='id of the image', location='args')

getsensordata_parser = reqparse.RequestParser()
getsensordata_parser.add_argument('time', type=int, required=False, help='Time of the data in Unix timestamp', location='args')
getsensordata_parser.add_argument('from_time', type=int, required=False, help='From time of the data in Unix timestamp', location='args')
getsensordata_parser.add_argument('to_time', type=int, required=False, help='To time of the data in Unix timestamp', location='args')

postsensordata_parser = reqparse.RequestParser()
postsensordata_parser.add_argument('food_weight', type=int, required=True, help='Weight of the food in grams', location='args')