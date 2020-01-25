import datetime
import pickle
import tempfile
from io import BytesIO
from random import randint

import h5py
import numpy as np
import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import matplotlib.pyplot as pyplot
from sklearn.model_selection import train_test_split
from tensorflow_core.core.protobuf.config_pb2 import ConfigProto
#from tensorflow_core.python.client.session import Session
from tensorflow_core.python.keras.backend import set_session
from tensorflow_core.python.keras.layers.core import Dense, Activation, Dropout
from tensorflow_core.python.keras.layers.cudnn_recurrent import CuDNNLSTM
from tensorflow_core.python.keras.layers.recurrent import LSTM
from tensorflow_core.python.keras.utils import np_utils
from datetime import datetime

from Normalizer import Normalizer


class RecurrentNeuralNetwork:

    model_file_format = '.bin'
    #normalizer = Normalizer()

    def __init__(self, data_set, unique_events_list, sequence_length=20, first_lstm_layer_size=256,
                 second_lstm_layer_size=256, dropout_rate=0.3):
        #tf.compat.v1.disable_eager_execution()

        #tf.compat.v1.config.experimental.set_memory_growth
        #max_memory = 1000  # dedicated memory in MB; run 'dxdiag' to get exact figure
        #max_usage = 0.95 * max_memory  # example for using up to 95%
        #config = ConfigProto()
        #config.gpu_options.allow_growth = True
        #sess = tf.compact.v1.Session(config=config)
        #set_session(sess)
        # gpus = tf.config.experimental.list_physical_devices('GPU')
        # tf.config.experimental.set_virtual_device_configuration(
        #     gpus[0],
        #     [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=max_usage)])
        self.data_set = data_set
        self.unique_events_list = unique_events_list
        self.sequence_length = sequence_length
        self.model = tf.keras.models.Sequential()
        self.first_lstm_layer_size = first_lstm_layer_size
        self.second_lstm_layer_size = second_lstm_layer_size
        self.dropout_rate = dropout_rate
        self.log_name = 'sl=' + str(sequence_length) + '1lstm=' + str(first_lstm_layer_size) + '2lstm='\
                        + str(second_lstm_layer_size) + 'drop' + str(dropout_rate)

    def prepare_model(self, number_of_unique_output_values):
        self.model.add(CuDNNLSTM(self.first_lstm_layer_size, batch_input_shape=(None, self.sequence_length, 1), return_sequences=True))
        self.model.add(Dropout(self.dropout_rate))
        self.model.add(CuDNNLSTM(self.second_lstm_layer_size))
        self.model.add(Dropout(self.dropout_rate))
        #self.model.add(Dense(self.dense_layer_size))
        #self.model.add(Dropout(self.dropout_rate))
        self.model.add(Dense(number_of_unique_output_values))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, number_of_epochs=100, test_size=0.2, callbacks=[]):
        self.log_name = self.log_name + 'epochs=' + str(number_of_epochs) + 'test=' + str(test_size)
        log_dir = "logs\\new_results\\" + self.log_name + '_' + datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
        csv_callback = tf.keras.callbacks.CSVLogger(filename=log_dir + 'logs.csv')
        callbacks.append(tensorboard_callback)
        callbacks.append(csv_callback)

        x = []
        y = []
        for track in self.data_set:
            for j in range(0, len(track) - self.sequence_length):
                input_vector = []
                for i in range(self.sequence_length):
                    input_vector.append(track[i + j]/self.unique_events_list.get_event_list_size())
                x.append(input_vector)
                y.append(track[j + self.sequence_length])

        self.prepare_model(self.unique_events_list.get_event_list_size())
        x = np.reshape(x, (len(x), self.sequence_length, 1))
        y = np_utils.to_categorical(y)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=1)

        history = self.model.fit(x_train, y_train, epochs=number_of_epochs, batch_size=32, callbacks=callbacks,
                                 validation_data=(x_test, y_test))
        pyplot.plot(history.history['loss'])
        pyplot.plot(history.history['val_loss'])
        pyplot.show()

    def answer(self, messages):
        normalized_messages = []
        for message in messages:
            normalized_messages.append([message/self.unique_events_list.get_event_list_size()])
        normalized_messages = np.array([normalized_messages], np.dtype(float))
        result = self.model.predict(normalized_messages)
        result = np.argmax(result)
        return result

    def save_model(self, path):
        with h5py.File('does not matter', driver='core', backing_store=False, mode='w') as h5file:
            tf.keras.models.save_model(self.model, h5file)
            h5file.flush()
            binary_data = h5file.id.get_file_image()
            object_for_save = {"binary_data": binary_data,
                               "data_set": self.data_set,
                               "sequence_length": self.sequence_length,
                               "unique_events_list": self.unique_events_list}
            with open(path, mode='wb') as handle:
                pickle.dump(object_for_save, handle)

    @staticmethod
    def load_model(path):
        with open(path, mode='rb') as handle:
            loaded_object = pickle.load(handle)
            model_file_object = BytesIO(loaded_object['binary_data'])
            data_set = loaded_object['data_set']
            sequence_length = loaded_object['sequence_length']
            unique_events_list = loaded_object['unique_events_list']
            result = RecurrentNeuralNetwork(data_set=data_set, unique_events_list=unique_events_list,
                                            sequence_length=sequence_length)
            with h5py.File(model_file_object, mode='r') as h5file:
                result.model = tf.keras.models.load_model(h5file)
            return result

    def generate(self, length):
        #random_track = self.data_set[randint(0, len(self.data_set) - 1)]
        #original_fragment_start = randint(0, len(random_track) - self.sequence_length - 1)
        #notes = random_track[original_fragment_start:original_fragment_start+self.sequence_length]
        #print(self.unique_events_list.get_event_list_size())
        #print(random_track[original_fragment_start+self.sequence_length:original_fragment_start+self.sequence_length+length])
        
        notes = []
        for i in range(0, self.sequence_length):
            notes.append(randint(0, self.unique_events_list.get_event_list_size()))

        print(notes)
        for i in range(0, length):
            train_messages = notes[-self.sequence_length:]
            notes.append(self.answer(train_messages))
        notes = notes[self.sequence_length:]
        print(notes)
        return notes

