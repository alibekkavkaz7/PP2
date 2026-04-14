import pygame
import os


def play(self):
    if len(self.tracks) == 0:
        print("Нет файлов")
        return

    pygame.mixer.music.load(os.path.join(self.folder, self.tracks[self.index]))
    pygame.mixer.music.play()

class Player:
    def __init__(self, folder):
        self.folder = folder
        self.tracks = os.listdir(folder)
        self.index = 0

    def play(self):
        pygame.mixer.music.load(os.path.join(self.folder, self.tracks[self.index]))
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()
    