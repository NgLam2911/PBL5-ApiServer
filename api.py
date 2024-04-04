from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse
import werkzeug
import os
import app_utils
import uuid as uuid_generator
from image_proccessor import ImageProcessor
from PIL import Image
import pandas as pd
from io import BytesIO

app = Flask(__name__)
api = Api(app)
proccessor = ImageProcessor()
hostname = 'nglam.xyz'
if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('predict'):
    os.makedirs('predict')

class UploadImage(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
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
    
class GetImage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str, required=True, help='id is required', location='args')
        args = parser.parse_args()
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
            "id": "0",
            "uuid": f"{uuid}",
            "url": f"http://{hostname}/image/{uuid}",
            "predict": f"http://{hostname}/predict/{uuid}",
            "labels": labels,
            "chicken": chicken,
            "sick_chicken": sick_chicken,
            "other": other
        }
    
class GetImages(Resource):
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
                    "id": f"{id}",
                    "uuid": f"{uuid}",
                    "url": f"http://{hostname}/image/{uuid}",
                    "predict": f"http://{hostname}/predict/{uuid}",
                    "labels": labels,
                    "chicken": chicken,
                    "sick_chicken": sick_chicken,
                    "other": other
                })
                id += 1
        return data
    
class GetLastImage(Resource):
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
            "id": "0",
            "uuid": f"{last}",
            "url": f"http://{hostname}/image/{last}",
            "predict": f"http://{hostname}/predict/{last}",
            "labels": labels,
            "chicken": chicken,
            "sick_chicken": sick_chicken,
            "other": other
        }
    
@app.route('/image/<uuid>')
def image(uuid):
    filename = f'images/{uuid}.png'
    if not os.path.exists(filename):
        return {'message': 'Image not found'}, 404
    if not os.path.isfile(filename):
        return {'message': 'Invalid image'}, 400
    return send_file(filename, mimetype='image/jpeg')

@app.route('/predict/<uuid>')
def predict(uuid):
    filename = f'images/{uuid}.png'
    if not os.path.exists(filename):
        return {'message': 'Image not found'}, 404
    if not os.path.isfile(filename):
        return {'message': 'Invalid image'}, 400
    if not os.path.exists(f'predict/{uuid}.csv'):
        df = proccessor.predict(Image.open(filename))
        df.to_csv(f'predict/{uuid}.csv', index=False)
    else:
        df = pd.read_csv(f'predict/{uuid}.csv')
    result_image = proccessor.plot(Image.open(filename), df)
    # convert the image to a byte array
    img_io = BytesIO()
    result_image.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
    
api.add_resource(UploadImage, '/upload')
api.add_resource(GetImage, '/getimage')
api.add_resource(GetImages, '/getimages')
api.add_resource(GetLastImage, '/getlastimage')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
        