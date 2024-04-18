import torch
from PIL import Image
import numpy as np
import cv2
from pandas import DataFrame
from app_utils import Singleton


class ImageProcessor(Singleton):
    
    model_path = "data/model/model.pt"
    model_type = "WongKinYiu/yolov7"
    model_name = "custom"
    
    def __init__(self):
        # load yolov7 model from model_path
        if not hasattr(self, 'model'):
            # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.model = torch.hub.load(self.model_type, self.model_name, self.model_path, trust_repo=True, force_reload=True)
            self.model.eval()
        pass
    
    # Return pandas dataframe
    def predict(self, image: Image):
        with torch.no_grad():
            result = self.model(image)
        prediction = result.pandas().xyxy[0]
        return prediction
            
    @staticmethod
    def plot(img: Image, prediction: DataFrame):
        image_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        for _, row in prediction.iterrows():
            xmin, ymin, xmax, ymax = map(int, row[['xmin', 'ymin', 'xmax', 'ymax']])
            label = row['name']
            # Draw the rectangle on the image depending on the label
            if label == "chicken":
                # green
                box_color = (0, 255, 0)
            elif label == "sick_chicken":
                # red
                box_color = (255, 0, 0)
            else:
                # gray
                box_color = (128, 128, 128)
            cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), box_color, 2)
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