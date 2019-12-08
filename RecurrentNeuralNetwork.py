from queue import Queue

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as pyplot
from sklearn.model_selection import train_test_split


class RecurrentNeuralNetwork:

    model = tf.keras.models.Sequential()

    def __init__(self):
        self.model.add(tf.keras.layers.LSTM(2, activation='relu', batch_input_shape=(None, 3, 2), return_sequences=False))

        self.model.compile(loss='mse', optimazer='adam', metrics=['accuracy'])

    def train(self, data_set):
        x = [[data_set[i + j] for i in range(3)] for j in range(0, len(data_set) - 3)]
        y = [data_set[i + 3] for i in range(0, len(data_set) - 3)]

        print(x)

        x = tf.keras.utils.normalize(x)
        y = tf.keras.utils.normalize(y)

        x = np.array(x, np.dtype(float))
        y = np.array(y, np.dtype(float))

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

        print(x.shape)
        history = self.model.fit(x_train, y_train, epochs=100)
        pyplot.plot(history.history['loss'])
        pyplot.show()

    def answer(self, messages):
        messages = tf.keras.utils.normalize(messages)
        messages = np.array(messages, np.dtype(float))
        return self.model.predict([messages])

    def save_model(self):
        self.model.save('models/model.h5')

    def load_model(self):
        self.model = tf.keras.models.load_model('models/model.h5')

    def generate(self, length):
        notes = [[56.0, 0.0], [64.0, 1440.0], [64.0, 1440.0]]
        for i in range(0, length):
            train_messages = [[notes[-3], notes[-2], notes[-1]]]
            print(train_messages)
            notes.append(self.answer(train_messages)[0].tolist())

        result = [[int(note[0]), int[note[1]]] for note in notes]
        return result

