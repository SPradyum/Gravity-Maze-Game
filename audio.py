import pygame
import os

class AudioSystem:
    def __init__(self):
        pygame.mixer.init()
        self.music_folder = os.path.join("assets", "music")
        self.sfx_folder = os.path.join("assets", "sfx")
        self.cache = {}

    def play_music(self, filename, volume=0.4):
        try:
            path = os.path.join(self.music_folder, filename)
            if not os.path.exists(path):
                return
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def play_sfx(self, filename, volume=0.6):
        try:
            if filename not in self.cache:
                path = os.path.join(self.sfx_folder, filename)
                if not os.path.exists(path):
                    return
                self.cache[filename] = pygame.mixer.Sound(path)
            snd = self.cache[filename]
            snd.set_volume(volume)
            snd.play()
        except Exception:
            pass
