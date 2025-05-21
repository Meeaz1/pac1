# player.py
import pygame
from settings import WIDTH, HEIGHT, player_speed

def draw_player(screen, player_images, direction, counter, player_x, player_y):
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    img = player_images[counter // 5]
    if direction == 0:
        screen.blit(img, (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(img, True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(img,  90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(img, 270), (player_x, player_y))

def check_position(level, centerx, centery, direction):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    num3 = 15

    if centerx // num2 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3)//num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3)//num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3)//num1][centerx //num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3)//num1][centerx //num2] < 3:
                turns[2] = True

        if direction in (2,3):
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3)//num1][centerx//num2] <3:
                    turns[3] = True
                if level[(centery - num3)//num1][centerx//num2] <3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx - num2)//num2] <3:
                    turns[1] = True
                if level[centery//num1][(centerx + num2)//num2] <3:
                    turns[0] = True

        if direction in (0,1):
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1)//num1][centerx//num2] <3:
                    turns[3] = True
                if level[(centery - num1)//num1][centerx//num2] <3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery//num1][(centerx - num3)//num2] <3:
                    turns[1] = True
                if level[centery//num1][(centerx + num3)//num2] <3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(direction, turns_allowed, player_x, player_y):
    if direction == 0 and turns_allowed[0]:
        player_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        player_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        player_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        player_y += player_speed
    return player_x, player_y
