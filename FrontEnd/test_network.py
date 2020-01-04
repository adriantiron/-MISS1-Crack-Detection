from keras.models import load_model
import numpy as np
import os, cv2

images = list()
predictions = list()


def get_nn_data():
    data = dict()
    model = load_model('model.h5')
    layers = ""
    for layer in model.layers:
        layers += layer.__class__.__name__
        layers += " "
    data['Layers'] = layers
    data['Input shape'] = str(model.inputs[0].shape)
    data['Input type'] = str(model.inputs[0].dtype)
    data['Output shape'] = str(model.outputs[0].shape)
    data['Output type'] = str(model.outputs[0].dtype)

    data['Test path'] = path
    data['Test images'] = str(images)
    data['Predictions'] = str(predictions)
    data['Positives number'] = str(len(list(x for x in predictions if x < .5)))
    data['Negatives number'] = str(len(list(x for x in predictions if x >= .5)))
    return data


# 0 = POSITIVE, 1 = NEGATIVE
def predict(image_path):
    model = load_model('model.h5')

    img_sz = 128
    image = cv2.resize(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), (img_sz, img_sz))
    image = np.array(image).reshape(1, img_sz, img_sz, 1) / 255.0
    prediction = model.predict(image)
    closeness = prediction[0][0]

    global path
    path, image_name = os.path.split(image_path)
    images.append(image_name)
    predictions.append(closeness)

    if round(closeness) == 0:
        classification = "POSITIVE CRACK"
    else:
        classification = "NEGATIVE CRACK"

    return "{} class closeness: {} to class {}".format(os.path.basename(image_path), closeness, classification)


# print(predict("E:\\Programs\\Coding\\ASET Crack Detection\\Dataset\\Test\\Positive\\039.png"))
