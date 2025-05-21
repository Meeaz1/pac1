# settings.py
import pygame
import math

pygame.init()

# экран
WIDTH  = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer  = pygame.time.Clock()
fps    = 60

# шрифты и цвета
font  = pygame.font.Font('freesansbold.ttf', 20)
color = 'blue'
PI    = math.pi

# скорость игрока
player_speed = 3
