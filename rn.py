from keras.models import Sequential
from keras.layers import Dense, Dropout, InputLayer
from keras.optimizers import SGD
from keras.regularizers import l2

import _pickle as cPickle, gzip, numpy as np
f = gzip.open('res/mnist.pkl.gz', 'rb')
(train_x, train_y), (val_x, val_y), (test_x, test_y) = cPickle.load(f, encoding='latin')
f.close()

targets = np.eye(10)
train_y, val_y, test_y = [targets[y] for y in [train_y, val_y, test_y]]

model = Sequential()
model.add(InputLayer((784,)))
model.add(Dropout(0.3))
model.add(Dense(100, activation='sigmoid', kernel_regularizer=l2(0.01)))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer=SGD(0.3, momentum=True), loss='categorical_crossentropy', metrics=['acc'])
# optimizer='rmsprop'

model.fit(train_x, train_y, validation_data=(val_x, val_y), epochs=5, batch_size=32)
preds = model.predict(test_x[:4])
print(test_y[:4])
print(preds)
loss, acc = model.evaluate(test_x, test_y)
print("Loss: {} Acc: {}".format(loss, acc))
