import torch
from PIL import Image
import numpy as np
import cv2
from pandas import DataFrame
from utilties import Singleton
from config import Config
from ultralytics import YOLO
import pandas as pd

class ImageProcessor(Singleton):
    config = Config()
    model_path = config.model_path()
    model_type = config.model_type()
    model_name = config.model_name()
    
    def __init__(self):
        # load yolo model from model_path
        if not hasattr(self, 'model'):
            # Because of ultralytics/ultralytics doesnt fully support pytorch hub.
            if self.model_type == "ultralytics/yolo":
                self.model = YOLO(self.model_path)
                pass
            else:
                # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                self.model = torch.hub.load(self.model_type, self.model_name, self.model_path, trust_repo=True, force_reload=True)
                self.model.eval()
        pass
    
    def ultralytics_to_pandas(self, results):
        boxes_list = results[0].boxes.data.tolist()
        columns = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']

        for i in boxes_list:
            i[:4] = [round(i, 1) for i in i[:4]]
            i[5] = int(i[5])
            i.append(results[0].names[i[5]])
        columns.append('name')
        result_df = pd.DataFrame(boxes_list, columns=columns)
        return result_df
    
    # Return pandas dataframe
    def predict(self, image: Image, conf: float = 0.6):
        if self.model_type == "ultralytics/yolo":
            result = self.model(image)
            prediction = self.ultralytics_to_pandas(result)
            # Filter out predictions with confidence less than `conf`
            prediction = prediction[prediction['confidence'] >= conf]
        else:
            with torch.no_grad():
                result = self.model(image)
            prediction = result.pandas().xyxy[0]
            # Filter out predictions with confidence less than `conf`
            prediction = prediction[prediction['confidence'] >= conf]
        return prediction
            
    @staticmethod
    def plot(img: Image, prediction: DataFrame):
        image_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        for _, row in prediction.iterrows():
            xmin, ymin, xmax, ymax = map(int, row[['xmin', 'ymin', 'xmax', 'ymax']])
            label = row['name']
            # Draw the rectangle on the image depending on the label
            if label == "chicken":
                # black
                box_color = (0, 0, 0)
            elif label == "sick_chicken":
                # red
                box_color = (255, 0, 0)
            else:
                # gray
                box_color = (128, 128, 128)
            cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), box_color, 4)
            # Put the label on the image
            cv2.putText(image_cv, label, (xmin + 5, ymin + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        # Convert back to PIL Image and return
        image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        return image
    
    @staticmethod
    def getLabelInfo(prediction: DataFrame):
        labels, chicken, sick_chicken, other = 0,0,0,0
        labels = len(prediction)
        for _, row in prediction.iterrows():
            label = row['name']
            if label == "chicken":
                chicken += 1
            elif label == "sick_chicken":
                sick_chicken += 1
            else:
                other += 1
        return labels, chicken, sick_chicken, other