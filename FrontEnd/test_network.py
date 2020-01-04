from keras.models import load_model
import numpy as np
import os, cv2


# 0 = POSITIVE, 1 = NEGATIVE
def predict(image_path):
    model = load_model('model.h5')

    img_sz = 128
    image = cv2.resize(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), (img_sz, img_sz))
    image = np.array(image).reshape(1, img_sz, img_sz, 1) / 255.0
    prediction = model.predict(image)

    closeness = prediction[0][0]
    if round(closeness) == 0:
        classification = "POSITIVE CRACK"
    else:
        classification = "NEGATIVE CRACK"

    return "{} class closeness: {} to class {}".format(os.path.basename(image_path), closeness, classification)


print(predict("E:\\Programs\\Coding\\ASET Crack Detection\\Dataset\\Test\\Positive\\039.png"))
