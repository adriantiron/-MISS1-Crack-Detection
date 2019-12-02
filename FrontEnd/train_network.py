import keras.models, keras.layers
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np, glob
from PIL import Image


def retrain_nn():
    model = keras.models.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        keras.layers.MaxPool2D((2, 2)),
        keras.layers.Conv2D(32, (3, 3), activation='relu'),
        keras.layers.MaxPool2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPool2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(units=512, activation='relu'),
        keras.layers.Dense(units=1, activation='sigmoid'),
    ])

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])

    aug = ImageDataGenerator(
        rotation_range=30,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")

    train_dir = "../Dataset/Train"
    validation_dir = "../Dataset/Test"
    batch_size = 300
    train_length = 38000
    validation_length = 2000

    train_generator = aug.flow_from_directory(train_dir,
                                              target_size=(128, 128),
                                              batch_size=batch_size,
                                              class_mode='binary')

    validation_generator = aug.flow_from_directory(validation_dir,
                                                   target_size=(128, 128),
                                                   batch_size=batch_size,
                                                   class_mode='binary')

    train = model.fit_generator(
          train_generator,
          steps_per_epoch=int(train_length / batch_size),
          epochs=1,
          verbose=1,
          validation_data=validation_generator,
          validation_steps=int(validation_length / batch_size)
    )

    model.save('model.h5')
