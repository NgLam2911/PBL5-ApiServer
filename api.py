from flask import Blueprint
from flask_restx import Api, Resource, fields
import werkzeug
import os
import uuid as uuid_generator
from data_proccessor import DataProcessor
from PIL import Image
import pandas as pd
import parsers
from database import Database
import time as timelib
from config import Config

app = Blueprint('api', __name__, url_prefix='/api')
api = Api(app, version='0.2.3', title='AI Server API')
db = Database()
image_api = api.namespace('image', description='Image operations')
proccessor = DataProcessor()
config = Config()

if not os.path.exists(config.image_path()):
    os.makedirs(config.image_path())
if not os.path.exists(config.predict_path()):
    os.makedirs(config.predict_path())
    
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
        raw_amg = args['amg']
        if not isinstance(image_file, werkzeug.datastructures.FileStorage):
            return {'message': 'No file part'}, 400
        uuid = str(uuid_generator.uuid4())
        file_path = config.image_path() + f'/{uuid}.png'
        image_file.save(file_path)
        time = int(timelib.time())
        db.setLastUUID(uuid)
        # process image and save the result
        image = Image.open(file_path)
        amg = [float(i) for i in raw_amg[1:-1].split(',')]
        df = proccessor.predict(image, amg)
        # save the result to a file
        df.to_csv(config.predict_path() + f'/{uuid}.csv', index=False)
        db.addImageData(time, uuid, raw_amg)
        print(f'Got image: {uuid}')
        return {
            'message': 'Image uploaded successfully',
            'uuid': uuid
        }, 200
        
image_respond_model = api.model('ImageRespond', {
    'id': fields.Integer(description='ID of the image'),
    'uuid': fields.String(description='UUID of the image'),
    'url': fields.String(description='URL of the image'),
    'predict': fields.String(description='URL of the prediction'),
    'infared': fields.String(description='URL of the infared image'),
    'raw-amg': fields.String(description='Raw IR camera sensor data of the image'),
    'time': fields.Integer(description='Time of the image'),
    'highest_chicken_temp': fields.Float(description='Highest temperature of the chicken in the image'),
    'labels': fields.String(description='Labels of the image'),
    'chicken': fields.String(description='Number of chicken'),
    'non-chicken': fields.String(description='Number of other')
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
        image_path = config.image_path() + f'/{uuid}.png'
        predict_path = config.predict_path() + f'/{uuid}.csv'
        if not os.path.exists(image_path):
            return {'message': 'Image not found'}, 404
        if not os.path.isfile(image_path):
            return {'message': 'Invalid image'}, 400
        imagedata = db.getImageDataByUUID(uuid)
        raw_amg = imagedata['amg']
        if not os.path.exists(predict_path):
            amg = [float(i) for i in raw_amg[1:-1].split(',')]
            df = proccessor.predict(Image.open(image_path), amg)
            df.to_csv(predict_path, index=False)
        else:
            df = pd.read_csv(predict_path)
        labels, chicken, non_chicken = proccessor.getLabelInfo(df)
        time = imagedata['time']
        hct = proccessor.highest_chicken_temp(df)
        return {
            "id": 0,
            "uuid": f"{uuid}",
            "url": f"http://{config.hostname()}/image/{uuid}",
            "predict": f"http://{config.hostname()}/predict/{uuid}",
            'infared': f"http://{config.hostname()}/infared/{uuid}",
            "raw-amg": raw_amg,
            "time": time,
            "highest_chicken_temp": hct,
            "labels": labels,
            "chicken": chicken,
            "non-chicken": non_chicken
        }, 200 

# Get all images
@image_api.route('/getall')
@api.doc(description='Get all images')
class GetImages(Resource):
    @api.response(200, 'Images found', [image_respond_model])
    def get(self):
        data = []
        id = 0
        for filename in os.listdir(config.image_path()):
            if filename.endswith('.png'):
                uuid = filename.split('.')[0]
                imagedata = db.getImageDataByUUID(uuid)
                raw_amg = imagedata['amg']
                amg = [float(i) for i in raw_amg[1:-1].split(',')]
                if not os.path.exists(config.predict_path() + f'/{uuid}.csv'):
                    df = proccessor.predict(Image.open(config.image_path() + f'/{uuid}.png'), amg)
                    df.to_csv(config.predict_path() + f'/{uuid}.csv', index=False)
                else:
                    df = pd.read_csv(config.predict_path() + f'/{uuid}.csv')
                labels, chicken, non_chicken = proccessor.getLabelInfo(df)
                time = imagedata['time']
                hct = proccessor.highest_chicken_temp(df)
                data.append({
                    "id": id,
                    "uuid": f"{uuid}",
                    "url": f"http://{config.hostname()}/image/{uuid}",
                    "predict": f"http://{config.hostname()}/predict/{uuid}",
                    'infared': f"http://{config.hostname()}/infared/{uuid}",
                    "raw-amg": raw_amg,
                    "time": time,
                    "highest_chicken_temp": hct,
                    "labels": labels,
                    "chicken": chicken,
                    "non-chicken": non_chicken
                })
                id += 1
        return data, 200
    
@image_api.route('/getbytime')
@api.doc(description='Get images by time')
class GetImagesByTime(Resource):
    @api.expect(parsers.getimagetime_parser)
    @api.response(200, 'Images found', [image_respond_model])
    def get(self):
        args = parsers.getimagetime_parser.parse_args()
        time = args['time']
        from_time = args['from_time']
        to_time = args['to_time']
        data = db.getImageData(time, from_time, to_time)
        result = []
        id = 0
        for i in data:
            uuid = i['uuid']
            if not os.path.exists(config.image_path() + f'/{uuid}.png'):
                continue
            raw_amg = i['amg']
            amg = [float(i) for i in raw_amg[1:-1].split(',')]
            if not os.path.exists(config.predict_path() + f'/{uuid}.csv'):
                df = proccessor.predict(Image.open(config.image_path() + f'/{uuid}.png'), amg)
                df.to_csv(config.predict_path() + f'/{uuid}.csv', index=False)
            else:
                df = pd.read_csv(config.predict_path() + f'/{uuid}.csv')
            labels, chicken, non_chicken = proccessor.getLabelInfo(df)
            time = i['time']
            hct = proccessor.highest_chicken_temp(df)
            result.append({
                "id": id,
                "uuid": f"{uuid}",
                "url": f"http://{config.hostname()}/image/{uuid}",
                "predict": f"http://{config.hostname()}/predict/{uuid}",
                'infared': f"http://{config.hostname()}/infared/{uuid}",
                "raw-amg": raw_amg,
                "time": time,
                "highest_chicken_temp": hct,
                "labels": labels,
                "chicken": chicken,
                "non-chicken": non_chicken
            })
            id += 1
        return result, 200

@image_api.route('/last')
@api.doc(description='Get the last image')
class GetLastImage(Resource):
    @api.response(200, 'Image found', image_respond_model)
    @api.response(404, 'No images found', image_respond_model_fail)
    def get(self):
        last = db.getLastUUID()
        if last == '0':
            return {'message': 'No images found'}, 404
        imagedata = db.getImageDataByUUID(last)
        raw_amg = imagedata['amg']
        amg = [float(i) for i in raw_amg[1:-1].split(',')]
        if not os.path.exists(config.predict_path() + f'/{last}.csv'):
            df = proccessor.predict(Image.open(config.image_path() + f'/{last}.png'), amg)
            df.to_csv(config.predict_path() + f'/{last}.csv', index=False)
        else:
            df = pd.read_csv(config.predict_path() + f'/{last}.csv')
        labels, chicken, non_chicken = proccessor.getLabelInfo(df)
        time = imagedata['time']
        hct = proccessor.highest_chicken_temp(df)
        return {
            "id": 0,
            "uuid": f"{last}",
            "url": f"http://{config.hostname()}/image/{last}",
            "predict": f"http://{config.hostname()}/predict/{last}",
            'infared': f"http://{config.hostname()}/infared/{last}",
            "raw-amg": raw_amg,
            "time": time,
            "highest_chicken_temp": hct,
            "labels": labels,
            "chicken": chicken,
            "non-chicken": non_chicken
        }, 200
        
sensor_api = api.namespace('sensor', description='Sensor operations')

sensor_data_respond = api.model('SensorDataRespond', {
    'time': fields.Integer(description='Time of the data'),
    'food_weight': fields.Float(description='Weight of the food in grams'),
    'water_weight': fields.Float(description='Weight of the water in grams')
})

sensor_data_post_success = api.model('SensorDataPostSuccess', {
    'message': fields.String(description='Message', default='Data added successfully')
})

sensor_data_post_fail = api.model('SensorDataPostFail', {
    'message': fields.String(description='Message', default='Invalid food weight')
})

@sensor_api.route('/')
class SensorData(Resource):
    @api.expect(parsers.getsensordata_parser)
    @api.response(200, 'List of sensor data', [sensor_data_respond])
    @api.doc(description='Get sensor data in time or a range, if no time is provided, return all data')
    def get(self):
        args = parsers.getsensordata_parser.parse_args()
        time = args['time']
        from_time = args['from_time']
        to_time = args['to_time']
        data = db.getSensorData(time, from_time, to_time)
        return data, 200
    
    @api.expect(parsers.postsensordata_parser)
    @api.response(200, 'Data added successfully', sensor_data_post_success)
    @api.response(400, 'Invalid data', sensor_data_post_fail)
    @api.doc(description='Add sensor data')
    def post(self):
        args = parsers.postsensordata_parser.parse_args()
        time = int(timelib.time())
        food_weight = args['food_weight']
        water_weight = args['water_weight']
        if not isinstance(food_weight, float):
            return {'message': 'Invalid data'}, 400
        if not isinstance(water_weight, float):
            return {'message': 'Invalid data'}, 400
        db.addSensorData(time, food_weight, water_weight)
        return {'message': 'Data added successfully'}, 200
        
analyze_api = api.namespace('analyze', description='Analyze operations')

consumed_respond = api.model('ConsumedRespond', {
    'food_consumed': fields.Float(description='Food consumed in grams'),
    'water_consumed': fields.Float(description='Water consumed in grams')
})

@analyze_api.route('/consumed')
class Consumed(Resource):
    @api.expect(parsers.consumed_parser)
    @api.response(200, 'Food and water consumed', consumed_respond)
    @api.doc(description='Get the food and water consumed in a time range')
    def get(self):
        args = parsers.consumed_parser.parse_args()
        from_time = args['from_time']
        to_time = args['to_time']
        food, water = proccessor.resourcesConsumed(from_time, to_time)
        return {
            'food_consumed': food,
            'water_consumed': water
        }, 200