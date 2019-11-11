import keras.models, keras.layers
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np, glob
from PIL import Image


imgs = None
for filename in glob.glob('Images/*.jpg'):
    im = Image.open(filename).convert(mode='L').resize((128, 128))
    im = image.img_to_array(im)
    im = np.expand_dims(im, axis=0)
    try:
        imgs = np.vstack((imgs, np.array(im)))
    except:
        imgs = np.vstack([im])

''' 
first dimension is the number of images
following 2 dim (128, 128) are the size of an image
last dimension (1) means that each value is encased in square parentheses
'''
print(imgs.shape)

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


image = load_img("Images/00001.jpg")
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

aug = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest")

imageGen = aug.flow(image, batch_size=1, save_to_dir="Output",
                    save_prefix="image", save_format="jpg")

total = 100
current = 0
for img in imageGen:
    current += 1
    if current == total:
        break
