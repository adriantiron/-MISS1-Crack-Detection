from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.optimizers import SGD
from keras.regularizers import l2
import numpy as np, glob
from PIL import Image

imgs = []
for filename in glob.glob('debug-ds/pos/*.jpg'):
    im = Image.open(filename).convert(mode='L')
    imgs.append(np.asarray(im.getdata()))

targets = np.eye(10)
train_y, val_y, test_y = [targets[y] for y in [train_y, val_y, test_y]]

model = Sequential()
model.add(InputLayer((51529,)))
model.add(Dropout(0.3))
model.add(Dense(100, activation='sigmoid', kernel_regularizer=l2(0.01)))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer=SGD(0.3, momentum=True), loss='categorical_crossentropy', metrics=['acc'])
# optimizer='rmsprop'

model.fit(imgs, train_y, epochs=5, batch_size=32)
preds = model.predict(imgs[:4])
print(test_y[:4])
print(preds)
loss, acc = model.evaluate(imgs, test_y)
print("Loss: {} Acc: {}".format(loss, acc))
