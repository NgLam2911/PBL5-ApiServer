from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse
import werkzeug
import os
import utils
import uuid as uuid_generator

app = Flask(__name__)
api = Api(app)
hostname = 'nglam.xyz'


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
        utils.setLastUUID(uuid)
        # TODO: Move this to a separate file for labelling
        return {
            'message': 'Image uploaded successfully',
            'uuid': uuid
        }, 200
    
class GetImage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True, help='id is required', location='args')
        args = parser.parse_args()
        id = args['id']
        if not os.path.exists(f'images/{id}.png'):
            return {'message': 'Image not found'}, 404
        if not os.path.isfile(f'images/{id}.png'):
            return {'message': 'Invalid image'}, 400
        return {
            "id": f"{id}",
            "url": f"http://{hostname}/image/{id}"
        }
    
class GetImages(Resource):
    def get(self):
        data = []
        for filename in os.listdir('images'):
            if filename.endswith('.png'):
                id = filename.split('.')[0]
                data.append({
                    "id": f"{id}",
                    "url": f"http://{hostname}/image/{id}"
                })
        return data
    
class GetLastImage(Resource):
    def get(self):
        last = utils.getLastUUID()
        if last == '0':
            return {'message': 'No images found'}, 404
        return {
            "id": f"{last}",
            "url": f"http://{hostname}/image/{last}"
        }
    
@app.route('/image/<uuid>')
def image(uuid):
    filename = f'images/{uuid}.png'
    if not os.path.exists(filename):
        return {'message': 'Image not found'}, 404
    if not os.path.isfile(filename):
        return {'message': 'Invalid image'}, 400
    return send_file(filename, mimetype='image/jpeg')
    
api.add_resource(UploadImage, '/upload')
api.add_resource(GetImage, '/getimage')
api.add_resource(GetImages, '/getimages')
api.add_resource(GetLastImage, '/getlastimage')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
        