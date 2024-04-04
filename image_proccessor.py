import torch
import torchvision.transforms as transforms
from torchvision.transforms import Resize
from PIL import Image
import numpy as np
import cv2

class ImageProcessor:
    
    model_path = "model/model.pt"
    model_type = "WongKinYiu/yolov7"
    model_name = "custom"
    
    def __init__(self):
        # load yolov7 model from model_path
        self.model = torch.hub.load(self.model_type, self.model_name, self.model_path)
        self.model.eval()
        pass
    
    def predict(self, image: Image):
        image = Resize((1024 , 1024))(image)
        img = transforms.ToTensor()(image).unsqueeze(0)
        result = self.model(img)
        if isinstance(result, tuple):
            # If result is a tuple, take the first element
            result = result[0]

        # Convert the PIL Image to an OpenCV Image
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        original_width, original_height = image.size

        # Calculate the scale factors
        scale_x = 1024 / original_width
        scale_y = 1024 / original_height

        # Iterate over the bounding boxes in the result tensor
        for box in result[0]:
            # Scale the coordinates
            x1 = int(box[0].item() * scale_x)
            y1 = int(box[1].item() * scale_y)
            x2 = int(box[2].item() * scale_x)
            y2 = int(box[3].item() * scale_y)

            # Draw the rectangle on the image
            cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Convert back to PIL Image and return
        image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        return image