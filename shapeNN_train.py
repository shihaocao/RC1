import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
import numpy as np
from tqdm import tqdm
import cv2
from random import shuffle
import os
import matplotlib.pyplot as plt

batch_size = 128
num_classes = 3
epochs = 10
#Srikar
#TRAIN_DIR = 'C:/Users/Srikar/Documents/shapes_data'
#TEST_DIR = 'C:/Users/Srikar/Documents/TestData'

#Patrick
TRAIN_DIR = 'C:/Users/zz198/Desktop/RC/shapes_data'
TEST_DIR = 'C:/Users/zz198/Desktop/RC/testdata'
IMG_SIZE = 64
LR = 1e-3
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match

# input image dimensions
img_rows, img_cols = 60, 60

def label_img(img_name):
    #0: Neg, 1: Square, 2: Triangle
    if img_name[0] == 'n':
        return [1,0,0]
    if img_name[0] == 's':
        return [0,1,0]
    if img_name[0] == 't':
        return [0,0,1]


def create_train_data():
    training_data = []
    for i in tqdm(os.listdir(TRAIN_DIR)):
        label = label_img(i)
        path = os.path.join(TRAIN_DIR,i)
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        training_data.append([np.array(img),np.array(label)])
    shuffle(training_data)
    np.save('train_data.npy', training_data)
    return training_data

def process_test_data():
    testing_data = []
    for count,i in enumerate(tqdm(os.listdir(TEST_DIR))):
        path = os.path.join(TEST_DIR,i)
        img_num = count
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        testing_data.append([np.array(img), img_num])

    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data

# the data, split between train and test sets

#(x_train, y_train), (x_test, y_test) = mnist.load_data()

#x_train = x_train.reshape(60000,60,60,1)
#x_test = x_test.reshape(10000,60,60,1)

#print(x_test)

#print('x_train shape:', x_train.shape)
#print(x_train.shape[0], 'train samples')
#print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
#y_train = keras.utils.to_categorical(y_train, num_classes)
#y_test = keras.utils.to_categorical(y_test, num_classes)

training_images = create_train_data()
testing_images = process_test_data()
print(len(training_images))
tr_img_data = np.array([i[0] for i in training_images]).reshape(-1,64,64,1)
tr_lbl_data = np.array([i[1] for i in training_images])
tst_img_data = np.array([i[0] for i in testing_images]).reshape(-1,64,64,1)
tst_lbl_data = np.array([i[1] for i in testing_images])

'''
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(28,28,1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
'''

model = Sequential()

model.add(InputLayer(input_shape=[64,64,1]))
model.add(Conv2D(filters=32,kernel_size=5,strides=1,padding='same',activation='relu'))
model.add(MaxPool2D(pool_size=5,padding='same'))

model.add(Conv2D(filters=50,kernel_size=5,strides=1,padding='same',activation='relu'))
model.add(MaxPool2D(pool_size=5,padding='same'))

model.add(Conv2D(filters=80,kernel_size=5,strides=1,padding='same',activation='relu'))
model.add(MaxPool2D(pool_size=5,padding='same'))

model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(512, input_shape=(64,),activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(num_classes, activation='softmax'))
optimizer = Adam(lr=LR)

model.compile(optimizer=optimizer,loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(x=tr_img_data,y=tr_lbl_data,epochs=epochs,batch_size=100,verbose=1)
model.summary()

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

# evaluate loaded model on test data
fig=plt.figure(figsize=(14,14))

for cnt, data in enumerate(testing_images[10:40]):
    y = fig.add_subplot(6,5,cnt+1)
    img = data[0]
    data = img.reshape(1,64,64,1)
    model_out = model.predict([data])

    if np.argmax(model_out) == 0:
        str_label = 'Negative'
    elif np.argmax(model_out) == 1:
        str_label = 'Square'
    else:
        str_label = 'Triangle'

    y.imshow(img, cmap='gray')
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)

plt.show()
