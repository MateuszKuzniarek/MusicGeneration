from MidiConverter import MidiConverter
from MusicPlayer import MusicPlayer
from RecurrentNeuralNetwork import RecurrentNeuralNetwork
from UniqueEventsList import UniqueEventsList


class GeneratorFacade:

    def __init__(self):
        self.neural_network = None
        self.melody = None
        self.music_player = MusicPlayer()
        self.duration = None
        self.data_set = None
        self.unique_events_list = None

    def is_model_loaded(self):
        if self.neural_network is None:
            return False
        return True

    def is_melody_generated(self):
        if self.melody is None:
            return False
        return True

    def load_model(self, file_path):
        if not file_path:
            return False
        self.neural_network = RecurrentNeuralNetwork.load_model(file_path)
        return True

    def save_model(self, file_path):
        if file_path is None or self.neural_network is None:
            return
        self.neural_network.save_model(file_path)

    @staticmethod
    def get_model_file_format():
        return RecurrentNeuralNetwork.model_file_format

    def generate_melody(self, duration):
        if self.neural_network is None:
            return
        self.duration = duration
        ticks_per_second = (MidiConverter.ticks_per_beat * MidiConverter.beats_per_minute) / 60
        number_of_ticks = duration * ticks_per_second
        number_of_notes = number_of_ticks/MidiConverter.delta_time_in_ticks
        self.melody = self.neural_network.generate(int(number_of_notes))

    def save_melody(self, file_path):
        if self.melody is None:
            return
        MidiConverter.write_midi_file(file_path, self.melody, self.neural_network.unique_events_list)

    def play_melody(self):
        file_object = MidiConverter.get_midi_file_object(self.melody, self.neural_network.unique_events_list)
        self.music_player.play(file_object)
        print('play melody')

    def stop_melody(self):
        self.music_player.stop()
        print('stop melody')

    def load_data_set(self, file_paths):
        self.data_set = []
        for file_path in file_paths:
            self.data_set.append(MidiConverter.convert_midi_file(file_path))
        self.unique_events_list = UniqueEventsList(self.data_set)
        self.unique_events_list.convert_data_set(self.data_set)

    def reset_data_set(self):
        self.data_set = None

    def is_data_set_loaded(self):
        if self.data_set is not None:
            return True
        return False

    def train(self, sequence_length, lstm_layer_size, dense_layer_size,
              dropout_rate, number_of_epochs, test_sample_ratio, callbacks):
        self.neural_network = RecurrentNeuralNetwork(self.data_set, self.unique_events_list, sequence_length,
                                                     lstm_layer_size, dense_layer_size, dropout_rate)
        self.neural_network.train(number_of_epochs, test_sample_ratio, callbacks)




