import random
import pygame, pygame.time, pygame.display, pygame.event, pygame.draw, pygame.sprite, pygame.key, pygame.transform, \
    pygame.mixer
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame import image, font

pygame.init()

width, height = 800, 700

pygame.display.set_caption('PAC-MAN')
window_surface = pygame.display.set_mode((width, height))

background = pygame.Surface((width, height))
background.fill(pygame.Color(0, 0, 0))

blue_color = (0, 152, 254)
yellow_color = (253, 206, 2)
score_ = 0


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = pygame.transform.scale(image.load(player_image), (20, 20))
        self.rect = self.image.get_rect()  # !!!!!!!!!!!!
        self.rect.x = player_x
        self.rect.y = player_y
        self.change_x = 0
        self.change_y = 0
        self.angle_to_rotate = 0
        self.way_to_move = "UP"


class Player(GameSprite):

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.change_x = -1
            self.change_y = 0
            self.angle_to_rotate = 180
            self.way_to_move = 'LEFT'
            window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
                                (self.rect.x, self.rect.y))  # !!!!!!!!!!!!!!!

        elif keys[K_RIGHT]:
            self.change_x = 1
            self.change_y = 0
            self.angle_to_rotate = 0
            self.way_to_move = 'RIGHT'
            window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
                                (self.rect.x, self.rect.y))  # !!!!!!!!!!!!!!!

        elif keys[K_UP]:
            self.change_y = -1
            self.change_x = 0
            self.angle_to_rotate = 90
            self.way_to_move = 'UP'
            window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
                                (self.rect.x, self.rect.y))  # !!!!!!!!!!!!!!!

        elif keys[K_DOWN]:
            self.change_y = 1
            self.change_x = 0
            self.angle_to_rotate = -90
            self.way_to_move = 'DOWN'
            window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
                                (self.rect.x, self.rect.y))  # !!!!!!!!!!!!!!!

        window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate), (self.rect.x, self.rect.y))

    def stop(self):
        self.change_x = 0
        self.change_y = 0


class Enemy(GameSprite):

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.way_to_move == "RIGHT":
            self.change_x = 1
            self.change_y = 0
            # self.angle_to_rotate = 0
            # window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
            #                     (self.rect.x, self.rect.y))
        elif self.way_to_move == "LEFT":
            self.change_x = -1
            self.change_y = 0
            # self.angle_to_rotate = 180
            # window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
            #                     (self.rect.x, self.rect.y))
        elif self.way_to_move == "UP":
            self.change_x = 0
            self.change_y = -1
            # self.angle_to_rotate = 90
            # window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
            #                     (self.rect.x, self.rect.y))
        elif self.way_to_move == "DOWN":
            self.change_x = 0
            self.change_y = 1
            # self.angle_to_rotate = -90
            # window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate),
            #                     (self.rect.x, self.rect.y))

        ran_var = ("RIGHT", "UP", "DOWN", "LEFT")

        if pygame.sprite.spritecollide(self, all_walls, False):
            for wall1 in all_walls:

                if self.rect.left == wall1.rect.right or self.rect.left == wall1.rect.left:
                    self.change_x = 0
                    self.rect.x += 7
                    self.way_to_move = random.choice(("RIGHT", "UP", "DOWN"))
                elif self.rect.right == wall1.rect.right:
                    self.change_x = 0
                    self.rect.x -= 7
                    self.way_to_move = random.choice(("UP", "DOWN", "LEFT"))
                elif self.rect.top == wall1.rect.right or self.rect.top == wall1.rect.top:
                    self.change_y = 0
                    self.rect.y += 7
                    self.way_to_move = random.choice(("RIGHT", "DOWN", "LEFT"))
                elif self.rect.bottom == wall1.rect.right:
                    self.change_y = 0
                    self.rect.y -= 7
                    self.way_to_move = random.choice(("RIGHT", "UP", "LEFT"))

        window_surface.blit(pygame.transform.rotate(self.image, self.angle_to_rotate), (self.rect.x, self.rect.y))

    def stop(self):
        self.change_x = 0
        self.change_y = 0


class Wall(pygame.sprite.Sprite):
    def __init__(self, wall_color, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(wall_color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        background.blit(self.image, (self.rect.x, self.rect.y))


class Money(pygame.sprite.Sprite):
    global player, coin

    def __init__(self, coin_color, coin_x, coin_y, coin_width, coin_height):
        super().__init__()
        self.width = coin_width
        self.height = coin_height
        self.coin_color = coin_color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(coin_color)
        self.rect = self.image.get_rect()
        self.rect.x = coin_x
        self.rect.y = coin_y

    # self.money_sound = pygame.mixer.Sound('collect_coin.mp3')
    def draw_coin(self):
        background.blit(self.image, (self.rect.x, self.rect.y))


def map():
    grid = ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 7, 1, 1, 3, 1, 1, 1, 8, 0, 7, 1, 1, 1, 3, 1, 1, 8, 0, 0, 0, 0),
            (0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0),
            (0, 0, 0, 0, 5, 1, 1, '0', 1, 3, 1, 4, 1, 4, 1, 3, 1, '0', 1, 1, 6, 0, 0, 0, 0),
            (0, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0),
            (0, 0, 0, 0, 9, 1, 1, 6, 0, 9, 1, 8, 0, 7, 1, 10, 0, 5, 1, 1, 10, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 7, 1, 4, 'f', 4, 1, 8, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 1, 1, '0', 1, 6, 0, 0, 0, 0, 0, 5, 1, '0', 1, 1, 1, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 5, 1, 1, 1, 1, 1, 6, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 7, 1, 1, '0', 1, 4, 1, 8, 0, 7, 1, 4, 1, '0', 1, 1, 8, 0, 0, 0, 0),
            (0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0),
            (0, 0, 0, 0, 9, 8, 0, 5, 1, 3, 1, 4, 1, 4, 1, 3, 1, 6, 0, 7, 10, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 7, 4, 1, 10, 0, 9, 1, 8, 0, 7, 1, 10, 0, 9, 1, 4, 8, 0, 0, 0, 0),
            (0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0),
            (0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 4, 1, 4, 1, 1, 1, 1, 1, 1, 10, 0, 0, 0, 0))
    return grid


all_walls = pygame.sprite.Group()
all_coins = pygame.sprite.Group()


def draw_map(screen):
    global blue_color, yellow_color

    wall_size = 2
    wall_long = 33
    for i, row in enumerate(map()):
        for j, item in enumerate(row):
            if item == 1:  # top and bottom
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32 + 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 2:  # left and right
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32 + 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 3:  # top
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

            elif item == 4:  # bottom
                pygame.draw.line(screen, blue_color, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32 + 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

            elif item == 5:  # left
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

            elif item == 6:  # right
                pygame.draw.line(screen, blue_color, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32 + 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

            elif item == 7:  # top left
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 8:  # top right
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32 + 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 9:  # bottom left
                pygame.draw.line(screen, blue_color, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32 + 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 10:  # bottom right
                pygame.draw.line(screen, blue_color, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32 + 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

                pygame.draw.line(screen, blue_color, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)

                wall = Wall(blue_color, j * 32 + 32, i * 32, wall_size, wall_long)
                wall.draw_wall()
                all_walls.add(wall)

            elif item == 'f':  # finish
                pygame.draw.line(screen, blue_color, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)

                wall = Wall(blue_color, (j * 32) - 1, i * 32, wall_long, wall_size)
                wall.draw_wall()
                all_walls.add(wall)

                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)

            elif item == '0':
                coin = Money(yellow_color, (j * 32) + 13, i * 32 + 13, 6, 6)
                coin.draw_coin()
                all_coins.add(coin)


draw_map(background)  # Малюємо карту
all_enemy = pygame.sprite.Group()
player = Player('pacman-25735.png', width / 2 - 8, (height - (height / 2)) - 120)
enemy1 = Enemy('fantasmas-pacman-png-1-Transparent-Images.png', width / 2 - 8, (height - (height / 2)) - 50)
enemy2 = Enemy('fantasmas-de-pacman-png-4-Transparent-Images.png', width / 2 - 12, (height - (height / 2)) - 60)
enemy3 = Enemy('6640981_preview.png', width / 2 - 15, (height - (height / 2)) - 65)

all_enemy.add(enemy1)
all_enemy.add(enemy2)
all_enemy.add(enemy3)
clock = pygame.time.Clock()
is_running = True
all_coins_collected = False
font = pygame.font.Font('freesansbold.ttf', 26)


def show_score(x, y):
    score = font.render("Score : " + str(score_), True, (255, 255, 255))
    window_surface.blit(score, (x, y))


def stop():
    player.stop()
    enemy2.stop()
    enemy3.stop()
    enemy1.stop()


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    window_surface.blit(over_text, (width / 2 - 80, (height - (height / 2)) - 65))
    stop()


def win_text():
    over_text = font.render("YOU WIN", True, (255, 255, 255))
    window_surface.blit(over_text, (width / 2 - 80, (height - (height / 2)) - 65))
    stop()


while is_running:

    window_surface.blit(background, (0, 0))
    pygame.transform.flip(background, True, False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    for coin in all_coins:
        if pygame.sprite.collide_rect(player, coin):
            score_ += 1
            all_coins.remove(coin)
            coin = Money((0, 0, 0), coin.rect.x, coin.rect.y, 6, 6)
            coin.draw_coin()
    for enem in all_enemy:
        if pygame.sprite.collide_rect(player, enem):
            game_over_text()
            break
    if len(all_coins) == 0:
        win_text()
        break

    if not all_coins_collected:
        for wall in all_walls:
            if pygame.sprite.collide_rect(player, wall):
                if player.way_to_move == 'LEFT':
                    player.change_x = 0
                    player.rect.x += 3
                elif player.way_to_move == 'RIGHT':
                    player.change_x = 0
                    player.rect.x -= 3
                elif player.way_to_move == 'UP':
                    player.change_y = 0
                    player.rect.y += 3
                elif player.way_to_move == 'DOWN':
                    player.change_y = 0
                    player.rect.y -= 3

        all_enemy.update()
        player.update()
    show_score(5, 5)
    pygame.display.update()
    clock.tick(60)