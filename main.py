from MidiConverter import MidiConverter
from RecurrentNeuralNetwork import RecurrentNeuralNetwork

converted_midi = MidiConverter.convert_midi_file('test_files/test2.mid')

#for i in converted_midi:
#    print(i)

#print(len(converted_midi))
#x = [[converted_midi[i+j] for i in range(3)] for j in range(0, len(converted_midi)-2)]
#y = [converted_midi[i+3] for i in range(0, len(converted_midi)-3)]
#print(x)
#print(y)
#print(converted_midi)

x = RecurrentNeuralNetwork()
#x.train(converted_midi)
#x.save_model()
x.load_model()

#notes = [[56.0, 0.0], [64.0, 1440.0], [64.0, 1440.0]]
#a = x.answer(notes)
#print(a)
generated_notes = x.generate(300)
#MidiConverter.write_midi_file('out_test', generated_notes)