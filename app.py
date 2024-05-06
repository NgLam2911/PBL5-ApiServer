from flask import send_file, render_template, Blueprint
import os
from image_proccessor import ImageProcessor
from PIL import Image
import pandas as pd
from io import BytesIO
from config import Config
from database import Database

app = Blueprint("web", __name__, url_prefix="/")
proccessor = ImageProcessor()
config = Config()
db = Database()
# Route to the index page first
@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/image/<uuid>')
def image(uuid):
    filename = config.image_path() + f'/{uuid}.png'
    if not os.path.exists(filename):
        return {'message': 'Image not found'}, 404
    if not os.path.isfile(filename):
        return {'message': 'Invalid image'}, 400
    return send_file(filename, mimetype='image/jpeg'), 200

@app.route('/predict/<uuid>')
def predict(uuid):
    filename = config.image_path() + f'/{uuid}.png'
    if not os.path.exists(filename):
        return {'message': 'Image not found'}, 404
    if not os.path.isfile(filename):
        return {'message': 'Invalid image'}, 400
    if not os.path.exists(config.predict_path() + f'/{uuid}.csv'):
        df = proccessor.predict(Image.open(filename))
        df.to_csv(config.predict_path() + f'/{uuid}.csv', index=False)
    else:
        df = pd.read_csv(config.predict_path() + f'/{uuid}.csv')
    result_image = proccessor.plot(Image.open(filename), df)
    # convert the image to a byte array
    img_io = BytesIO()
    result_image.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg'), 200

@app.route('/infared/<uuid>')
def infared(uuid):
    imagedata = db.getImageDataByUUID(uuid)
    if not imagedata:
        return {'message': 'Image not found'}, 404
    raw_amg = imagedata['amg'] 
    amg = [float(i) for i in raw_amg[1:-1].split(',')]
    result_image = proccessor.ir2image(amg)
    # convert the image to a byte array
    img_io = BytesIO()
    result_image.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg'), 200
        