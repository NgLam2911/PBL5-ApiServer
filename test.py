from image_proccessor import ImageProcessor
from PIL import Image

proccessor = ImageProcessor()

image = Image.open("data/images/f688d659-17bb-4e40-833b-53ae671edb1e.png")
df = proccessor.predict(image)
print(df)