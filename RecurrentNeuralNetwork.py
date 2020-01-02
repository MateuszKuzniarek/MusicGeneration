import pickle
import tempfile
from io import BytesIO
from random import randint

import h5py
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as pyplot
from sklearn.model_selection import train_test_split
from tensorflow_core.python.keras.layers.core import Dense, Activation, Dropout
from tensorflow_core.python.keras.layers.cudnn_recurrent import CuDNNLSTM
from tensorflow_core.python.keras.utils import np_utils

from Normalizer import Normalizer


class RecurrentNeuralNetwork:

    model_file_format = '.bin'
    #normalizer = Normalizer()
    sequence_length = 20

    def __init__(self):
        self.data_set = None
        self.model = tf.keras.models.Sequential()
        self.model.add(CuDNNLSTM(512, batch_input_shape=(None, self.sequence_length, 1), return_sequences=True))
        self.model.add(Dropout(0.3))
        self.model.add(CuDNNLSTM(512))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(256))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(90))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    def train(self, data_set):
        self.data_set = data_set
        x = []
        y = []
        for track in data_set:
            for j in range(0, len(track) - self.sequence_length):
                input_vector = []
                for i in range(self.sequence_length):
                    input_vector.append(track[i + j]/127)
                x.append(input_vector)
                y.append(track[j + self.sequence_length])

        x = np.reshape(x, (len(x), self.sequence_length, 1))
        y = np_utils.to_categorical(y)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

        history = self.model.fit(x_train, y_train, epochs=200, batch_size=64)
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
        with h5py.File('does not matter', driver='core',
                       backing_store=False, mode='w') as h5file:
            tf.keras.models.save_model(self.model, h5file)
            h5file.flush()
            binary_data = h5file.id.get_file_image()
            object_for_save = {"binary_data": binary_data, "data_set": self.data_set}
            pickle.dump(object_for_save, open(path, mode='wb'))

    def load_model(self, path):
        loaded_object = pickle.load(open(path, mode='rb'))
        model_file_object = BytesIO(loaded_object['binary_data'])
        with h5py.File(model_file_object, mode='r') as h5file:
            self.model = tf.keras.models.load_model(h5file)
        self.data_set = loaded_object['data_set']

    def generate(self, length):
        random_track = self.data_set[randint(0, len(self.data_set) - 1)]
        original_fragment_start = randint(0, len(random_track) - self.sequence_length - 1)
        notes = random_track[original_fragment_start:original_fragment_start+self.sequence_length]
        for i in range(0, length):
            train_messages = notes[-self.sequence_length:]
            notes.append(self.answer(train_messages))
        notes = notes[self.sequence_length:]
        print(notes)
        return notes

