# utils.py
import pygame

def load_player_images():
    player_images = []
    for i in range(1, 5):
        img = pygame.image.load(f'assets/player_images/{i}.png')
        img = pygame.transform.scale(img, (45, 45))
        player_images.append(img)
    return player_images

def load_ghost_images():
    blinky_img = pygame.image.load('assets/ghost_images/red.png')
    pinky_img  = pygame.image.load('assets/ghost_images/pink.png')
    inky_img   = pygame.image.load('assets/ghost_images/blue.png')
    clyde_img  = pygame.image.load('assets/ghost_images/orange.png')
    blinky_img = pygame.transform.scale(blinky_img, (45,45))
    pinky_img  = pygame.transform.scale(pinky_img,  (45,45))
    inky_img   = pygame.transform.scale(inky_img,   (45,45))
    clyde_img  = pygame.transform.scale(clyde_img,  (45,45))
    return blinky_img, pinky_img, inky_img, clyde_img
