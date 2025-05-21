import pygame
import os

SOUND_DIR = r"C:\Users\meeaz\PycharmProjects\PythonProject\PythonPacman-main\sound"

# Глобальные переменные для управления звуком waka (в начале файла, рядом с импортами)
waka_playing = False
waka_eating = False
waka_stop_timer = 0


class SoundManager:
    def __init__(self):
        self.sounds = {
            "waka": pygame.mixer.Sound(os.path.join(SOUND_DIR, "waka.wav")),
            "intro": pygame.mixer.Sound(os.path.join(SOUND_DIR, "intro.wav")),
            "victory": pygame.mixer.Sound(os.path.join(SOUND_DIR, "victory.wav")),
            "death": pygame.mixer.Sound(os.path.join(SOUND_DIR, "death.wav")),
        }
        self.channel_waka = pygame.mixer.Channel(0)

    def play_waka(self, loops=0):
        # Проигрываем звук waka на выделенном канале с циклом loops
        self.channel_waka.play(self.sounds["waka"], loops=loops)

    def stop_waka(self):
        # Плавно останавливаем звук waka
        self.channel_waka.fadeout(300)

    def play_intro(self):
        self.sounds["intro"].play()
        pygame.time.delay(int(self.sounds["intro"].get_length() * 1000))  # ждём окончания интро

    def play_victory(self):
        self.sounds["victory"].play()

    def play_death(self):
        self.sounds["death"].play()
