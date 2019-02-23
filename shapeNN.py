import keras
from keras.datasets import mnist
from keras.models import Sequential, model_from_json
from keras.layers import *
from keras.optimizers import *
import numpy as np
from tqdm import tqdm
import cv2
from random import shuffle
import os
import matplotlib as plt

batch_size = 128
num_classes = 3
epochs = 15
TRAIN_DIR = 'C:/Users/Srikar/Documents/shapes_data'
TEST_DIR = 'C:/Users/Srikar/Documents/TestData'
IMG_SIZE = 64
LR = 1e-3
MODEL_NAME = 'dogsvscats-{}-{}.model'.format(LR, '2conv-basic') # just so we remember which saved model is which, sizes must match

# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

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

training_images = create_train_data()
testing_images = process_test_data()
print(len(training_images))
tr_img_data = np.array([i[0] for i in training_images]).reshape(-1,64,64,1)
tr_lbl_data = np.array([i[1] for i in training_images])
tst_img_data = np.array([i[0] for i in testing_images]).reshape(-1,64,64,1)
tst_lbl_data = np.array([i[1] for i in testing_images])

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


#loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#score = loaded_model.evaluate(X, Y, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
