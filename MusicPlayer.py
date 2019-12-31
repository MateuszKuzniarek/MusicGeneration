import pygame


class MusicPlayer:

    def __init__(self):
        pygame.init()

    def play(self, file_object):
        file_object.seek(0)
        pygame.mixer.music.load(file_object)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
