import mido
from mido import MidiTrack, MidiFile, Message


class MidiConverter:

    output_path = "output_files/"

    @staticmethod
    def display_midi_file(path):
        mid = MidiFile(path)
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
                    notes.append([msg.note, msg.time])

        return notes

    @staticmethod
    def write_midi_file(name, notes):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        for note in notes:
            track.append(Message('note_on', note=note[0], velocity=64, time=note[1]))

        mid.save(MidiConverter.output_path + name)
