import pickle
import time
from concurrent.futures import thread

import tensorflow

from GeneratorFacade import GeneratorFacade
from MainWindow import MainWindow
from MidiConverter import MidiConverter
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




generator_facade = GeneratorFacade()

window = MainWindow(generator_facade)
window.display_window()