import torch
import pandas as pd
from image_proccessor import ImageProcessor
from PIL import Image

processor = ImageProcessor()
image_path = "aria-76.jpg"
image = Image.open(image_path)
result = processor.predict(image)
result.save("highlighted_image.jpg")