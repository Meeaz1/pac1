# main.py
import copy
import pygame

from settings import *
from board import boards
from utils import load_player_images, load_ghost_images
from player import draw_player, move_player, check_position
from ghost import Ghost

def main():
    # ——— Инициализация ———
    pygame.init()
    level = copy.deepcopy(boards)
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    timer = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 20)

    player_images   = load_player_images()
    blinky_img, pinky_img, inky_img, clyde_img = load_ghost_images()

    # стартовые координаты
    player_x, player_y = 450, 663
    direction, direction_command = 0, 0

    blinky_x, blinky_y, blinky_direction = 56, 58, 0
    inky_x,   inky_y,   inky_direction   = 440,388,2
    pinky_x,  pinky_y,  pinky_direction  = 440,438,2
    clyde_x,  clyde_y,  clyde_direction  = 440,438,2

    # остальные флаги
    counter = 0
    flicker = False
    score = 0
    powerup = False
    power_counter = 0
    eaten_ghost = [False]*4
    blinky_dead = inky_dead = pinky_dead = clyde_dead = False
    blinky_box = inky_box = pinky_box = clyde_box = False
    moving = False
    ghost_speeds = [2]*4
    startup_counter = 0
    lives = 3
    game_over = False
    game_won = False

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))

    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)

    for i in range(lives):
        icon = pygame.transform.scale(player_images[0], (30,30))
        screen.blit(icon, (650 + i*40, 915))

    if game_over:
        pygame.draw.rect(screen, 'white',      [50,200,800,300],0,10)
        pygame.draw.rect(screen, 'dark gray', [70,220,760,260],0,10)
        t = font.render('Гру закінчено! Пробіл для рестарту!', True, 'red')
        screen.blit(t, (100,300))

    if game_won:
        pygame.draw.rect(screen, 'white',      [50,200,800,300],0,10)
        pygame.draw.rect(screen, 'dark gray', [70,220,760,260],0,10)
        t = font.render('Перемога! Пробіл для рестарту!', True, 'green')
        screen.blit(t, (100,300))

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50)//32
    num2 = WIDTH//30

    if 0 < player_x < 870:
        if level[center_y//num1][center_x//num2] == 1:
            level[center_y//num1][center_x//num2] = 0
            scor += 10
        if level[center_y//num1][center_x//num2] == 2:
            level[center_y//num1][center_x//num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False]*4

    return scor, power, power_count, eaten_ghosts

def draw_board():
    num1 = (HEIGHT - 50)//32
    num2 = WIDTH//30

    for i in range(len(level)):
        for j in range(len(level[i])):
            cell = level[i][j]
            x = j*num2 + 0.5*num2
            y = i*num1 + 0.5*num1

            if cell == 1:
                pygame.draw.circle(screen, 'white', (x,y), 4)
            if cell == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (x,y),10)
            if cell == 3:
                pygame.draw.line(screen, color, (x, i*num1),(x, i*num1+num1),3)
            if cell == 4:
                pygame.draw.line(screen, color, (j*num2, y),(j*num2+num2, y),3)
            if cell == 5:
                pygame.draw.arc(screen, color, [(j*num2 - num2*0.4)-2, y, num2, num1], 0, PI/2,3)
            if cell == 6:
                pygame.draw.arc(screen, color, [(j*num2 + num2*0.5), y, num2, num1], PI/2, PI,3)
            if cell == 7:
                pygame.draw.arc(screen, color, [(j*num2 + num2*0.5), i*num1 - num1*0.4, num2, num1], PI, 3*PI/2,3)
            if cell == 8:
                pygame.draw.arc(screen, color, [(j*num2 - num2*0.4)-2, i*num1 - num1*0.4, num2, num1], 3*PI/2, 2*PI,3)
            if cell == 9:
                pygame.draw.line(screen, 'white', (j*num2, y),(j*num2+num2, y),3)

def get_targets(blink_x, blink_y,
                ink_x,   ink_y,
                pink_x,  pink_y,
                clyd_x,  clyd_y):

    runaway_x = WIDTH if player_x < 450 else 0
    runaway_y = HEIGHT if player_y < 450 else 0
    return_target = (380, 400)

    # если power-up активен
    if powerup:
        # Блинки
        if not blinky_dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky_dead and eaten_ghost[0]:
            blink_target = (400, 100) if 340 < blink_x < 560 and 340 < blink_y < 500 else (player_x, player_y)
        else:
            blink_target = return_target

        # Инки
        if not inky_dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky_dead and eaten_ghost[1]:
            ink_target = (400, 100) if 340 < ink_x < 560 and 340 < ink_y < 500 else (player_x, player_y)
        else:
            ink_target = return_target

        # Пинки
        if not pinky_dead and not eaten_ghost[2]:
            pink_target = (player_x, runaway_y)
        elif not pinky_dead and eaten_ghost[2]:
            pink_target = (400, 100) if 340 < pink_x < 560 and 340 < pink_y < 500 else (player_x, player_y)
        else:
            pink_target = return_target

        # Клайд
        if not clyde_dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde_dead and eaten_ghost[3]:
            clyd_target = (400, 100) if 340 < clyd_x < 560 and 340 < clyd_y < 500 else (player_x, player_y)
        else:
            clyd_target = return_target

        # Power-up неактивен: все преследуют игрока
    else:
        blink_target = (400, 100) if not blinky_dead and 340 < blink_x < 560 and 340 < blink_y < 500 else (
            (player_x, player_y) if not blinky_dead else return_target)
        ink_target = (400, 100) if not inky_dead and 340 < ink_x < 560 and 340 < ink_y < 500 else (
            (player_x, player_y) if not inky_dead else return_target)
        pink_target = (400, 100) if not pinky_dead and 340 < pink_x < 560 and 340 < pink_y < 500 else (
            (player_x, player_y) if not pinky_dead else return_target)
        clyd_target = (400, 100) if not clyde_dead and 340 < clyd_x < 560 and 340 < clyd_y < 500 else (
            (player_x, player_y) if not clyde_dead else return_target)

        # Возвращаем ровно 4 целей
    return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    timer.tick(fps)
    # … draw_board(), draw_player(), get_targets(), создание Ghost, движение, обработка событий …
    pygame.display.flip()


    targets = get_targets(
        blinky_x, blinky_y,
        inky_x, inky_y,
        pinky_x, pinky_y,
        clyde_x, clyde_y
    )

    blinky = Ghost(
        blinky_x, blinky_y, targets[0], ghost_speeds[0],
        blinky_img, blinky_direction, blinky_dead, blinky_box, 0
    )
    inky = Ghost(
        inky_x, inky_y, targets[1], ghost_speeds[1],
        inky_img, inky_direction, inky_dead, inky_box, 1
    )
    pinky = Ghost(
        pinky_x, pinky_y, targets[2], ghost_speeds[2],
        pinky_img, pinky_direction, pinky_dead, pinky_box, 2
    )
    clyde = Ghost(
        clyde_x, clyde_y, targets[3], ghost_speeds[3],
        clyde_img, clyde_direction, clyde_dead, clyde_box, 3
    )


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                # сброс при рестарте
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x, player_y = 450, 663
                direction, direction_command = 0, 0
                blinky_x, blinky_y, blinky_direction = 56, 58, 0
                inky_x,   inky_y,   inky_direction   = 440, 388, 2
                pinky_x,  pinky_y,  pinky_direction  = 440, 438, 2
                clyde_x,  clyde_y,  clyde_direction  = 440, 438, 2
                eaten_ghost = [False] * 4
                blinky_dead = inky_dead = pinky_dead = clyde_dead = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    # переключаем направление, если можно
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    # «тоннель» для игрока
    if player_x > WIDTH:
        player_x = -47
    elif player_x < -50:
        player_x = WIDTH - 3

    # выводим привидений из «домика», если они мертвы и уже в нём
    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False


    timer.tick(fps)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False]*4

    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()

    center_x = player_x + 23
    center_y = player_y + 24

    if powerup:
        ghost_speeds = [1,1,1,1]
    else:
        ghost_speeds = [2,2,2,2]
    if eaten_ghost[0]: ghost_speeds[0] = 2
    if eaten_ghost[1]: ghost_speeds[1] = 2
    if eaten_ghost[2]: ghost_speeds[2] = 2
    if eaten_ghost[3]: ghost_speeds[3] = 2
    if blinky_dead:   ghost_speeds[0] = 4
    if inky_dead:     ghost_speeds[1] = 4
    if pinky_dead:    ghost_speeds[2] = 4
    if clyde_dead:    ghost_speeds[3] = 4

    game_won = True
    for row in level:
        if 1 in row or 2 in row:
            game_won = False

    pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player(screen, player_images, direction, counter, player_x, player_y)

    blinky = Ghost(blinky_x, blinky_y, [], ghost_speeds[0],
                   blinky_img, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky   = Ghost(inky_x,   inky_y,   [], ghost_speeds[1],
                   inky_img,   inky_direction,   inky_dead,
                   inky_box,   1)
    pinky  = Ghost(pinky_x,  pinky_y,  [], ghost_speeds[2],
                   pinky_img,  pinky_direction,  pinky_dead,
                   pinky_box,  2)
    clyde  = Ghost(clyde_x,  clyde_y,  [], ghost_speeds[3],
                   clyde_img,  clyde_direction,  clyde_dead,
                   clyde_box,  3)

    draw_misc()

    targets = get_targets(
        blinky_x, blinky_y,
        inky_x, inky_y,
        pinky_x, pinky_y,
        clyde_x, clyde_y
    )

    blinky = Ghost(
        blinky_x, blinky_y, targets[0], ghost_speeds[0],
        blinky_img, blinky_direction, blinky_dead, blinky_box, 0
    )
    inky   = Ghost(
        inky_x,   inky_y,   targets[1], ghost_speeds[1],
        inky_img,   inky_direction,   inky_dead,   inky_box,   1
    )
    pinky  = Ghost(
        pinky_x,  pinky_y,  targets[2], ghost_speeds[2],
        pinky_img,  pinky_direction,  pinky_dead,  pinky_box,  2
    )
    clyde  = Ghost(
        clyde_x,  clyde_y,  targets[3], ghost_speeds[3],
        clyde_img,  clyde_direction,  clyde_dead,  clyde_box,  3
    )


    turns_allowed = check_position(level, center_x, center_y, direction)

    if moving:
        player_x, player_y = move_player(direction, turns_allowed, player_x, player_y)

        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()

        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()

        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

    score, powerup, power_counter, eaten_ghost = \
        check_collisions(score, powerup, power_counter, eaten_ghost)

    if not powerup:
        if (pygame.draw.circle(screen, 'black', (center_x, center_y), 20,2).colliderect(blinky.rect) and not blinky.dead)\
        or (pygame.draw.circle(screen, 'black', (center_x, center_y), 20,2).colliderect(inky.rect) and not inky.dead)\
        or (pygame.draw.circle(screen, 'black', (center_x, center_y), 20,2).colliderect(pinky.rect) and not pinky.dead)\
        or (pygame.draw.circle(screen, 'black', (center_x, center_y), 20,2).colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives    -= 1
                startup_counter = 0
                powerup  = False
                power_counter = 0
                player_x, player_y = 450, 663
                direction, direction_command = 0, 0
                blinky_x, blinky_y, blinky_direction = 56, 58, 0
                inky_x,   inky_y,   inky_direction   = 440,388,2
                pinky_x,  pinky_y,  pinky_direction  = 440,438,2
                clyde_x,  clyde_y,  clyde_direction  = 440,438,2
                eaten_ghost = [False]*4
                blinky_dead = inky_dead = pinky_dead = clyde_dead = False
            else:
                game_over = True
                moving    = False
                startup_counter=0

    pygame.display.flip()

pygame.quit()

if __name__ == "__main__":
    main()
