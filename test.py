import torch
import pandas as pd
from image_proccessor import ImageProcessor
from PIL import Image
import matplotlib as plt
import numpy as np

processor = ImageProcessor()
image_path = "test2.jpg"
image = Image.open(image_path)
result = processor.predict(image)
print(type(result))

import cv2
import numpy as np

# Convert the PIL Image to an OpenCV Image
image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Iterate over the DataFrames in the result list
for df in result:
    # Iterate over the bounding boxes in the DataFrame
    for _, row in df.iterrows():
        # Convert the coordinates to integers
        xmin, ymin, xmax, ymax = map(int, row[['xmin', 'ymin', 'xmax', 'ymax']])
        label = row['name']

        # Draw the rectangle on the image
        box_color = (0, 255, 0)
        cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), box_color, 2)

        # Put the label on the image
        text_color = (255, 255, 255) # white
        cv2.putText(image_cv, label, (xmin + 5, ymin + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

# Convert back to PIL Image and return
image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
image.show()