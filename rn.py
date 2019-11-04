import keras.models, keras.layers
from keras.preprocessing import image
import numpy as np, glob
from PIL import Image

for filename in glob.glob('debug-ds/pos/*.jpg'):
    im = Image.open(filename).convert(mode='L').resize((128, 128))
    im = image.img_to_array(im)
    im = np.expand_dims(im, axis=0)
    try:
        imgs = np.vstack((imgs, np.array(im)))
    except NameError:
        imgs = np.vstack([im])

''' 
first dimension is the nb of images
following 2 dim (128, 128) are the size of an image
last dimension (1) means that each value is encased in square parentheses
'''
print(imgs.shape)
exit()

model = keras.models.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    keras.layers.MaxPool2D((2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPool2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPool2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(units=512, activation='relu'),
    keras.layers.Dense(units=1, activation='sigmoid'),
])

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])
