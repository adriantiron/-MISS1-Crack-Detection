from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
import os

model = load_model('model.h5')

folder_path = "Dataset/Test/Negative"

for image_name in os.listdir(folder_path):

    image_path = os.path.join(folder_path, image_name)
    image = load_img(image_path)
    image = image.resize((128, 128))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    images = np.vstack([image])

    prediction = model.predict(images)

    print("{} crack precision: {} %".format(image_path, prediction[0][0] * 100))
