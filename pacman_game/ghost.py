# ghost.py
import pygame
import copy
from board import boards
from settings import HEIGHT, WIDTH, screen

# своя копия карты для проверки стен
level = copy.deepcopy(boards)

# состояния “испуган” и “мертв”
spooked_img = pygame.transform.scale(
    pygame.image.load('assets/ghost_images/powerup.png'), (45, 45))
dead_img    = pygame.transform.scale(
    pygame.image.load('assets/ghost_images/dead.png'),    (45, 45))

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos    = x_coord
        self.y_pos    = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target   = target
        self.speed    = speed
        self.img      = img
        self.direction= direct
        self.dead     = dead
        self.in_box   = box
        self.id       = id
        self.turns, self.in_box = self.check_collisions()
        self.rect     = self.draw()

    def draw(self):

        import __main__
        powerup = __main__.powerup
        eaten_ghost = __main__.eaten_ghost

        import __main__
        powerup = __main__.powerup
        eaten_ghost = __main__.eaten_ghost

        if (not powerup and not self.dead) \
           or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img,    (self.x_pos, self.y_pos))
        ghost_rect = pygame.Rect(
            (self.center_x - 18, self.center_y - 18), (36, 36)
        )
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        turns = [False, False, False, False]

        if 0 < self.center_x // num2 < 29:
            if level[(self.center_y - num3)//num1][self.center_x//num2] == 9:
                turns[2] = True
            if level[self.center_y//num1][(self.center_x - num3)//num2] <3 \
               or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 \
                   and (self.in_box or self.dead)):
                turns[1] = True
            if level[self.center_y//num1][(self.center_x + num3)//num2] <3 \
               or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 \
                   and (self.in_box or self.dead)):
                turns[0] = True
            if level[(self.center_y + num3)//num1][self.center_x//num2] <3 \
               or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 \
                   and (self.in_box or self.dead)):
                turns[3] = True
            if level[(self.center_y - num3)//num1][self.center_x//num2] <3 \
               or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 \
                   and (self.in_box or self.dead)):
                turns[2] = True

            if self.direction in (2,3):
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3)//num1][self.center_x//num2] <3 \
                       or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[3] = True
                    if level[(self.center_y - num3)//num1][self.center_x//num2] <3 \
                       or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y//num1][(self.center_x - num2)//num2] <3 \
                       or (level[self.center_y//num1][(self.center_x - num2)//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[1] = True
                    if level[self.center_y//num1][(self.center_x + num2)//num2] <3 \
                       or (level[self.center_y//num1][(self.center_x + num2)//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[0] = True

            if self.direction in (0,1):
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3)//num1][self.center_x//num2] <3 \
                       or (level[(self.center_y + num3)//num1][self.center_x//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[3] = True
                    if level[(self.center_y - num3)//num1][self.center_x//num2] <3 \
                       or (level[(self.center_y - num3)//num1][self.center_x//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y//num1][(self.center_x - num3)//num2] <3 \
                       or (level[self.center_y//num1][(self.center_x - num3)//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[1] = True
                    if level[self.center_y//num1][(self.center_x + num3)//num2] <3 \
                       or (level[self.center_y//num1][(self.center_x + num3)//num2] == 9 \
                           and (self.in_box or self.dead)):
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False

        return turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            # … весь ваш оригинальный код для direction == 0 …
            pass  # <-- здесь был ваш код
        elif self.direction == 1:
            # … весь ваш оригинальный код для direction == 1 …
            pass
        elif self.direction == 2:
            # … ваш код для direction == 2 …
            pass
        elif self.direction == 3:
            # … ваш код для direction == 3 …
            pass

        # —————— wrap-around на границах экрана ——————
        if self.x_pos < -30:
            self.x_pos = WIDTH
        elif self.x_pos > WIDTH:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
                pass
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
