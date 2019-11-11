import keras.models, keras.layers
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np, glob
from PIL import Image

greyscale_images = None
for filename in glob.glob('FewImages/*.jpg'):
    im = Image.open(filename).convert(mode='L').resize((128, 128))
    im = image.img_to_array(im)
    im = np.expand_dims(im, axis=0)
    try:
        greyscale_images = np.vstack((imgs, np.array(im)))
    except:
        greyscale_images = np.vstack([im])

''' 
first dimension is the number of images
following 2 dim (128, 128) are the size of an image
last dimension (1) means that each value is encased in square parentheses
'''
print(greyscale_images.shape)
# from skimage.io import imsave
# imsave('res2.jpg', imgs[1])
# exit()

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

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])


# image = load_img("FewImages/00001.jpg")
# image = img_to_array(image)
# image = np.expand_dims(image, axis=0)

aug = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest")

# imageGen = aug.flow(image, batch_size=1, save_to_dir="Output",
#                     save_prefix="image", save_format="jpg")

# total = 100
# current = 0
# for img in imageGen:
#     current += 1
#     if current == total:
#         break

train_dir = "Dataset/Train"
validation_dir = "Dataset/Test"
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
      epochs=3,
      verbose=1,
      validation_data=validation_generator,
      validation_steps=int(validation_length / batch_size)
)

model.save('model.h5')
