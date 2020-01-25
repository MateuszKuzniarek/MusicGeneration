class UniqueEventsList:
    def __init__(self, data_set):
        music_events = set()

        for file in data_set:
            for event in file:
                music_events.add(frozenset(event))

        self.events_list = list(music_events)

    def get_notes(self, index):
        return self.events_list[index]

    def get_index(self, index):
        return self.events_list.index(index)

    def get_event_list_size(self):
        return len(self.events_list)

    def convert_data_set(self, data_set):
        for track in data_set:
            for i in range(0, len(track)):
                track[i] = self.get_index(track[i])


