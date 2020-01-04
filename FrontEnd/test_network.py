from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
import os, decorators, validators


@decorators.nn_decorator
def predict(image_path):
    model = load_model('model.h5')
    if not validators.valid_image(image_path):
        return "File is not image"
    
    img_sz = 128
    image = cv2.resize(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), (img_sz, img_sz))
    image = np.array(image).reshape(img_sz, img_sz, 1)
    prediction = model.predict(image)
    return "{} precision: {} %".format(os.path.basename(image_path), prediction[0][0] * 100)

