from io import BytesIO

import mido
from mido import MidiTrack, MidiFile, Message


class MidiConverter:

    ticks_per_beat = 480
    beats_per_minute = 120
    delta_time_in_ticks = ticks_per_beat

    @staticmethod
    def display_midi_file(path):
        mid = MidiFile(path)
        print(mid.ticks_per_beat)
        for track in mid.tracks:
            print(track)
            for msg in track:
                print(msg)

    @staticmethod
    def convert_midi_file(path):
        notes = []

        mid = mido.MidiFile(path)
        for track in mid.tracks:
            for msg in track:
                if not msg.is_meta and msg.type == 'note_on':
                    notes.append(msg.note)

        return notes

    @staticmethod
    def get_midi_file_object(notes):
        file_object = BytesIO()
        mid = MidiConverter.__create_midi_file(notes)
        mid.save(file=file_object)
        return file_object

    @staticmethod
    def write_midi_file(path, notes):
        mid = MidiConverter.__create_midi_file(notes)
        mid.save(path)

    @staticmethod
    def __create_midi_file(notes):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        for note in notes:
            track.append(Message('note_on', note=note, velocity=64, time=MidiConverter.delta_time_in_ticks))
        return mid
