import numpy as np
import tensorflow as tf
import matplotlib.pyplot as pyplot
from sklearn.model_selection import train_test_split
from tensorflow_core.python.keras.layers.core import Dense, Activation, Dropout
from tensorflow_core.python.keras.utils import np_utils

from Normalizer import Normalizer


class RecurrentNeuralNetwork:

    model_file_format = '.h5'
    normalizer = Normalizer()
    sequence_length = 20

    def __init__(self):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.LSTM(40, activation='relu', batch_input_shape=(None, self.sequence_length, 1), return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(tf.keras.layers.LSTM(40))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(256))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(94))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    def train(self, data_set):
        x = [[[data_set[i + j]/127] for i in range(self.sequence_length)] for j in range(0, len(data_set) - self.sequence_length)]
        y = [data_set[i + self.sequence_length] for i in range(0, len(data_set) - self.sequence_length)]

        x = np.reshape(x, (len(x), self.sequence_length, 1))
        y = np_utils.to_categorical(y)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

        history = self.model.fit(x_train, y_train, epochs=100)
        pyplot.plot(history.history['loss'])
        pyplot.show()

    def answer(self, messages):
        normalized_messages = []
        for message in messages:
            normalized_messages.append([message/127])
        normalized_messages = np.array([normalized_messages], np.dtype(float))
        result = self.model.predict(normalized_messages)
        result = np.argmax(result)
        return result

    def save_model(self, path):
        #pickle.dump(self.normalizer, open('models/model.bin', mode='wb'))
        self.model.save(path)

    def load_model(self, path):
        #self.normalizer = pickle.load(open('models/model.bin', mode='rb'))
        self.model = tf.keras.models.load_model(path)

    def generate(self, length):
        notes = [56, 59, 64, 64, 59, 56, 52, 52, 56, 56, 59, 59, 64, 64, 64, 64, 68, 68, 71, 71]
        for i in range(0, length):
            train_messages = notes[-self.sequence_length:]
            #print(train_messages)
            notes.append(self.answer(train_messages))
        notes = notes[self.sequence_length:]
        return notes

