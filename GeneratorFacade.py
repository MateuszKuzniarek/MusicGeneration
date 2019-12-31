from MidiConverter import MidiConverter
from MusicPlayer import MusicPlayer
from RecurrentNeuralNetwork import RecurrentNeuralNetwork


class GeneratorFacade:

    def __init__(self):
        self.neural_network = None
        self.melody = None
        self.music_player = MusicPlayer()
        self.duration = None

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
        self.neural_network = RecurrentNeuralNetwork()
        self.neural_network.load_model(file_path)
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
        MidiConverter.write_midi_file(file_path, self.melody)

    def play_melody(self):
        self.music_player.play()
        print('play melody')

    def stop_melody(self):
        self.music_player.stop()
        print('stop melody')




