import pygame


class MusicPlayer:

    def __init__(self):
        pygame.init()

    def play(self):
        pygame.mixer.music.load("./output_files/out.midi")
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
