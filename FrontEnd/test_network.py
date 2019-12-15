from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
import os, decorators


@decorators.nn_decorator
def predict(image_path):
    model = load_model('model.h5')
    image = load_img(image_path)
    image = image.resize((128, 128))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    images = np.vstack([image])
    prediction = model.predict(images)
    return "{} precision: {} %".format(os.path.basename(image_path), prediction[0][0] * 100)
