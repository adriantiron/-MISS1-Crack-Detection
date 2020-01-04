from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
import os, cv2, random, numpy as np
import validators


def model_init(img_size):
    model = Sequential()

    model.add(Conv2D(16, (3, 3), activation="relu", input_shape=(img_size, img_size, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(.3))

    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(.3))

    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(.3))

    model.add(Flatten())
    model.add(Dense(258, activation="relu"))

    model.add(Dense(1, activation="sigmoid"))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def data_prep(img_size):
    train_dir = "..\\Dataset\\Train"
    validation_dir = "..\\Dataset\\Test"
    categories = ["Positive", "Negative"]
    images_array = []
    val_array = []

    for category in categories:
        path = os.path.join(train_dir, category)
        val_path = os.path.join(validation_dir, category)
        class_num = categories.index(category)

        for img in os.listdir(path):
            filename, extension = os.path.splitext(img)
            if extension in ['.jpg', '.png']:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (img_size, img_size))
                images_array.append([new_array, class_num])

        for img in os.listdir(val_path):
            filename, extension = os.path.splitext(img)
            if extension in ['.jpg', '.png']:
                img_array = cv2.imread(os.path.join(val_path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (img_size, img_size))
                val_array.append([new_array, class_num])

    random.shuffle(images_array)
    random.shuffle(val_array)
    x_train = []
    y_train = []
    x_val = []
    y_val = []

    for image, label in images_array:
        x_train.append(image)
        y_train.append(label)

    for image, label in val_array:
        x_val.append(image)
        y_val.append(label)

    x_train = np.array(x_train).reshape(len(x_train), img_size, img_size, 1)
    x_val = np.array(x_val).reshape(len(x_val), img_size, img_size, 1)

    return x_train, y_train, x_val, y_val


def train_nn(model, x_train, y_train, x_val, y_val, batch_size, epochs_nu):
    # This will slightly warp and transform the images so we have more training data
    aug = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        zoom_range=0.15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest")
    aug.fit(x_train)
    aug.fit(x_val)

    # This saves the best model after an epoch, so we don't lose progress if it crashes
    checkpoint = ModelCheckpoint("keras-crack.model.h5", monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    train = model.fit(
        aug.flow(x_train, y_train, batch_size=batch_size),
        steps_per_epoch=len(x_train)/batch_size,
        epochs=epochs_nu,
        verbose=1,
        validation_data=aug.flow(x_val, y_val, batch_size=batch_size),
        validation_steps=len(x_val)/batch_size,
        callbacks=[checkpoint]
    )

    model.save(os.path.join(os.getcwd(), 'crack.model.h5'))


def retrain_nn(batch_sz, epochs_nu):
    img_size = 128

    xt, yt, xv, yv = data_prep(img_size)
    new_model = model_init(img_size)
    train_nn(new_model, xt, yt, xv, yv, batch_sz, epochs_nu)
