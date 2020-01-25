import glob
import pickle
import time
from concurrent.futures import thread
from io import BytesIO

import numpy
#from music21 import converter, instrument, note, chord
import h5py
import tensorflow as tf
from tensorflow_core.python.keras.utils import np_utils

from GeneratorFacade import GeneratorFacade
from MainWindow import MainWindow
from MidiConverter import MidiConverter
from ModelCreationWindow import ModelCreationWindow
from MusicPlayer import MusicPlayer
from RecurrentNeuralNetwork import RecurrentNeuralNetwork

# converted_midis = [MidiConverter.convert_midi_file('test_files/mozart/1.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/2.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/3.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/4.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/5.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/6.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/7.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/8.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/9.mid'),
#                    MidiConverter.convert_midi_file('test_files/mozart/10.mid')]
# for i in converted_midi:
#     print(i)
#
# print(len(converted_midi))
# x = [[converted_midi[i+j] for i in range(3)] for j in range(0, len(converted_midi)-2)]
# y = [converted_midi[i+3] for i in range(0, len(converted_midi)-3)]
# print(x)
# print(y)
# print(converted_midi)

# x = RecurrentNeuralNetwork()
# x.train(converted_midis)
# x.save_model('./models/mozart.bin')
# z = x.generate(100)
# print(z)
#
# x = RecurrentNeuralNetwork()
# x.data_set = [MidiConverter.convert_midi_file('test_files/test2.mid')]
# x.model = tensorflow.keras.models.load_model('./models/model2.h5')
# x.save_model('./models/old_new_model.bin')

# x = RecurrentNeuralNetwork()
# x.load_model('./models/x.bin')
#
# z = x.generate(100)
# print(z)
# m = MusicPlayer()
# m.play(MidiConverter.get_midi_file_object(z))
# time.sleep(1000)
#
#
# y = RecurrentNeuralNetwork()
# y.load_model('./models/new_model.bin')
# z = y.generate(100)
# print(z)
#
# notes = [[56], [64], [64]]
# a = x.answer(notes)
# print(a)
# generated_notes = x.generate(300)
# MidiConverter.write_midi_file('out_test', generated_notes)
#
# MidiConverter.display_midi_file('output_files/out_test.midi')

# generator_facade = GeneratorFacade()
#
# window = ModelCreationWindow(generator_facade)
# window.display_window()


# loaded_object = pickle.load(open('./models/mozart.bin', mode='rb'))
# model_file_object = BytesIO(loaded_object['binary_data'])
# data_set = loaded_object['data_set']
# sequence_length = 20
# result = RecurrentNeuralNetwork(data_set=data_set, sequence_length=sequence_length)
# with h5py.File(model_file_object, mode='r') as h5file:
#     result.model = tf.keras.models.load_model(h5file)
#
# result.save_model('./models/new_mozart.bin')


#MidiConverter.display_midi_file('./test_files/mozart/1.mid')

# g = GeneratorFacade()
# g.load_data_set(['./test_files/mozart/1.mid', './test_files/mozart/2.mid'])


# from UniqueEventsList import UniqueEventsList
#
# data_set = []
# for file in glob.glob("./test_files/mozart/*.mid"):
#
#     data_set.append(MidiConverter.convert_midi_file(file))
#
#
# unique_events_list = UniqueEventsList(data_set)
# print(unique_events_list.get_event_list_size())
#print(data_set[0])
# from UniqueEventsList import UniqueEventsList
#
# g = GeneratorFacade()
#
# data_set = []
# music_player = MusicPlayer()
# data_set.append(MidiConverter.convert_midi_file('./test_files/mozart/1.mid'))
# unique_events_list = UniqueEventsList(data_set)
# unique_events_list.convert_data_set(data_set)
#
# file_object = MidiConverter.get_midi_file_object(data_set[0], unique_events_list)
# music_player.play(file_object)
#
# print(data_set[0])
#
# time.sleep(10000)







# def get_notes():
#     """ Get all the notes and chords from the midi files in the ./midi_songs directory """
#     notes = []
#
#     for file in glob.glob("./test_files/mozart/*.mid"):
#         midi = converter.parse(file)
#
#         print("Parsing %s" % file)
#
#         notes_to_parse = None
#
#         try: # file has instrument parts
#             s2 = instrument.partitionByInstrument(midi)
#             notes_to_parse = s2.parts[0].recurse()
#         except: # file has notes in a flat structure
#             notes_to_parse = midi.flat.notes
#         #notes = []
#         for element in notes_to_parse:
#             if isinstance(element, note.Note):
#                 notes.append(str(element.pitch.midi))
#             elif isinstance(element, chord.Chord):
#                 notes.append('.'.join(str(n) for n in element.normalOrder))
#
#         #print(notes)
#
#     # with open('data/notes', 'wb') as filepath:
#     #     pickle.dump(notes, filepath)
#
#     return notes

# def prepare_sequences(notes, n_vocab):
#     """ Prepare the sequences used by the Neural Network """
#     sequence_length = 100
#
#     x = set(item for item in notes)
#     # get all pitch names
#     pitchnames = sorted(set(item for item in notes))
#
#      # create a dictionary to map pitches to integers
#     note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
#
#     network_input = []
#     network_output = []
#
#     # create input sequences and the corresponding outputs
#     for i in range(0, len(notes) - sequence_length, 1):
#         sequence_in = notes[i:i + sequence_length]
#         sequence_out = notes[i + sequence_length]
#         network_input.append([note_to_int[char] for char in sequence_in])
#         network_output.append(note_to_int[sequence_out])
#
#     n_patterns = len(network_input)
#
#     # reshape the input into a format compatible with LSTM layers
#     network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
#     # normalize input
#     network_input = network_input / float(n_vocab)
#
#     network_output = np_utils.to_categorical(network_output)
#
#     return (network_input, network_output)
#
#
# """ Train a Neural Network to generate music """
# notes = get_notes()
#
# #print(len(notes))
#
# # get amount of pitch names
# n_vocab = len(set(notes))
# print(n_vocab)

#network_input, network_output = prepare_sequences(notes, n_vocab)















#import platform
#print(platform.python_implementation())



#76 78
generator_facade = GeneratorFacade()

window = MainWindow(generator_facade)
window.display_window()