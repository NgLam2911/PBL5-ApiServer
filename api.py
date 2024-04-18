from flask import Blueprint
from flask_restx import Api, Resource, fields
import werkzeug
import os
import app_utils
import uuid as uuid_generator
from image_proccessor import ImageProcessor
from PIL import Image
import pandas as pd
import parsers

app = Blueprint('api', __name__, url_prefix='/api')
api = Api(app, version='0.1', title='AI Server API')

image_api = api.namespace('image', description='Image operations')

proccessor = ImageProcessor()
hostname = 'nglam.xyz'
if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('predict'):
    os.makedirs('predict')
    
upload_respond_model = api.model('UploadRespond', {
    'message': fields.String(description='Message', default="Image uploaded successfully"),
    'uuid': fields.String(description='UUID of the image', default="")
})

upload_respond_model_fail = api.model('UploadRespondFail', {
    'message': fields.String(description='Message', default="No file part")
})

@image_api.route('/upload')
@api.doc(description='Upload an image')
class UploadImage(Resource):
    @api.expect(parsers.upload_parser)
    @api.response(200, 'Image uploaded successfully', upload_respond_model)
    @api.response(400, 'No file part', upload_respond_model_fail)
    def post(self):
        args = parsers.upload_parser.parse_args()
        image_file = args['file']
        if not isinstance(image_file, werkzeug.datastructures.FileStorage):
            return {'message': 'No file part'}, 400
        uuid = str(uuid_generator.uuid4())
        file_path = f'images/{uuid}.png'
        image_file.save(file_path)
        app_utils.setLastUUID(uuid)
        # process image and save the result
        image = Image.open(file_path)
        df = proccessor.predict(image)
        # save the result to a file
        df.to_csv(f'predict/{uuid}.csv', index=False)
        return {
            'message': 'Image uploaded successfully',
            'uuid': uuid
        }, 200
        
image_respond_model = api.model('ImageRespond', {
    'id': fields.Integer(description='ID of the image'),
    'uuid': fields.String(description='UUID of the image'),
    'url': fields.String(description='URL of the image'),
    'predict': fields.String(description='URL of the prediction'),
    'labels': fields.String(description='Labels of the image'),
    'chicken': fields.String(description='Number of chicken'),
    'sick_chicken': fields.String(description='Number of sick chicken'),
    'other': fields.String(description='Number of other')
})

image_respond_model_fail = api.model('ImageRespondFail', {
    'message': fields.String(description='Message', default="Image not found")
})

@image_api.route('/get')
@api.doc(description='Get an image with uuid')
class GetImage(Resource):
    @api.expect(parsers.getimage_parser)
    @api.response(200, 'Image found', image_respond_model)
    @api.response(404, 'Image not found', image_respond_model_fail)
    @api.response(400, 'Invalid image', image_respond_model_fail)
    def get(self):
        args = parsers.getimage_parser.parse_args()
        uuid = args['uuid']
        if not os.path.exists(f'images/{uuid}.png'):
            return {'message': 'Image not found'}, 404
        if not os.path.isfile(f'images/{uuid}.png'):
            return {'message': 'Invalid image'}, 400
        if not os.path.exists(f'predict/{uuid}.csv'):
            df = proccessor.predict(Image.open(f'images/{uuid}.png'))
            df.to_csv(f'predict/{uuid}.csv', index=False)
        else:
            df = pd.read_csv(f'predict/{uuid}.csv')
        labels, chicken, sick_chicken, other = proccessor.getLabelInfo(pd)
        return {
            "id": 0,
            "uuid": f"{uuid}",
            "url": f"http://{hostname}/image/{uuid}",
            "predict": f"http://{hostname}/predict/{uuid}",
            "labels": labels,
            "chicken": chicken,
            "sick_chicken": sick_chicken,
            "other": other
        }, 200 

# Get all images
@image_api.route('/getall')
@api.doc(description='Get all images')
class GetImages(Resource):
    @api.response(200, 'Images found', [image_respond_model])
    def get(self):
        data = []
        id = 0
        for filename in os.listdir('images'):
            if filename.endswith('.png'):
                uuid = filename.split('.')[0]
                if not os.path.exists(f'predict/{uuid}.csv'):
                    df = proccessor.predict(Image.open(f'images/{uuid}.png'))
                    df.to_csv(f'predict/{uuid}.csv', index=False)
                else:
                    df = pd.read_csv(f'predict/{uuid}.csv')
                labels, chicken, sick_chicken, other = proccessor.getLabelInfo(df)
                data.append({
                    "id": id,
                    "uuid": f"{uuid}",
                    "url": f"http://{hostname}/image/{uuid}",
                    "predict": f"http://{hostname}/predict/{uuid}",
                    "labels": labels,
                    "chicken": chicken,
                    "sick_chicken": sick_chicken,
                    "other": other
                })
                id += 1
        return data, 200

@image_api.route('/last')
@api.doc(description='Get the last image')
class GetLastImage(Resource):
    @api.response(200, 'Image found', image_respond_model)
    @api.response(404, 'No images found', image_respond_model_fail)
    def get(self):
        last = app_utils.getLastUUID()
        if last == '0':
            return {'message': 'No images found'}, 404
        if not os.path.exists(f'predict/{last}.csv'):
            df = proccessor.predict(Image.open(f'images/{last}.png'))
            df.to_csv(f'predict/{last}.csv', index=False)
        else:
            df = pd.read_csv(f'predict/{last}.csv')
        labels, chicken, sick_chicken, other = proccessor.getLabelInfo(df)
        return {
            "id": 0,
            "uuid": f"{last}",
            "url": f"http://{hostname}/image/{last}",
            "predict": f"http://{hostname}/predict/{last}",
            "labels": labels,
            "chicken": chicken,
            "sick_chicken": sick_chicken,
            "other": other
        }, 200