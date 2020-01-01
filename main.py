import pickle
import time
from concurrent.futures import thread

import tensorflow

from GeneratorFacade import GeneratorFacade
from MainWindow import MainWindow
from MidiConverter import MidiConverter
from MusicPlayer import MusicPlayer
from RecurrentNeuralNetwork import RecurrentNeuralNetwork

#converted_midi = MidiConverter.convert_midi_file('test_files/test2.mid')

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
# x.train(converted_midi)
# x.save_model('./models/new_model.bin')
# z = x.generate(100)
# print(z)

# x = RecurrentNeuralNetwork()
# x.data_set = converted_midi
# x.model = tensorflow.keras.models.load_model('./models/model2.h5')
# x.save_model('./models/x.bin')

# x = RecurrentNeuralNetwork()
# x.load_model('./models/x.bin')

# z = x.generate(100)
# print(z)
# m = MusicPlayer()
# m.play(MidiConverter.get_midi_file_object(z))
# time.sleep(1000)

#
# y = RecurrentNeuralNetwork()
# y.load_model('./models/new_model.bin')
# z = y.generate(100)
# print(z)

#notes = [[56], [64], [64]]
#a = x.answer(notes)
#print(a)
#generated_notes = x.generate(300)
#MidiConverter.write_midi_file('out_test', generated_notes)

#MidiConverter.display_midi_file('output_files/out_test.midi')




generator_facade = GeneratorFacade()

window = MainWindow(generator_facade)
window.display_window()