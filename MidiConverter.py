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
        events = []
        #todo: multiple tracks problem
        mid = mido.MidiFile(path)
        for track in mid.tracks:
            for msg in track:
                if not msg.is_meta and msg.type == 'note_on':
                    if msg.time == 0 and events:
                        events[-1].add(msg.note)
                    else:
                        events.append({msg.note})
        return events

    @staticmethod
    def get_midi_file_object(notes, unique_events_list):
        file_object = BytesIO()
        mid = MidiConverter.__create_midi_file(notes, unique_events_list)
        mid.save(file=file_object)
        return file_object

    @staticmethod
    def write_midi_file(path, notes, unique_events_list):
        mid = MidiConverter.__create_midi_file(notes, unique_events_list)
        mid.save(path)

    @staticmethod
    def __create_midi_file(events, unique_events_list):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        for event in events:
            notes = list(unique_events_list.get_notes(event))
            track.append(Message('note_on', note=notes[0], velocity=64, time=MidiConverter.delta_time_in_ticks))
            if len(notes) > 1:
                for i in range(1, len(notes)):
                    track.append(Message('note_on', note=notes[i], velocity=64, time=0))
        return mid
