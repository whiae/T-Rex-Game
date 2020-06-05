import random
import pygame
from pygame.locals import *
import sys
import os
import math
import time

# define display surface
WIDTH = 1000
HEIGHT = 400
HW = WIDTH / 2
HH = HEIGHT / 2
AREA = WIDTH * HEIGHT

# define colors
WHITE = (255, 255, 255)
GREY = (247, 247, 247)
BLACK = (0, 0, 0)
GREEN = (0, 139, 69)
PINK = (255, 62, 150)

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# initialize pygame and create game window
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((WIDTH, HEIGHT))  # it sets the screen
pygame.display.set_caption("T-Rex Game")  # it sets the title of the game window
FPS = 120

background = pygame.image.load(os.path.join(img_folder, "ground.png")).convert()
x = 0

dinoCurrentImage = 0

font_name = pygame.font.match_font('Comic Sans MS')

# MUSIC
music = pygame.mixer.music.load('snd/music.mp3')
pygame.mixer.music.set_volume(0.15)
jump_sound = pygame.mixer.Sound('snd/jump.wav')
die_sound = pygame.mixer.Sound('snd/die.wav')


def draw_text(surf, text, size, x, y):
    # x i y to lokalizacja tekstu na ekranie
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_game_over_screen():
    draw_text(DS, "G A M E   O V E R", 20, WIDTH / 2, HEIGHT / 3)
    retry_img = pygame.image.load(os.path.join(img_folder, "retry.png")).convert()
    DS.blit(retry_img, (485, HEIGHT / 2))
    pygame.display.flip()


score = 0
high_score = 0

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12  # negative number, because it should slow us down
PLAYER_GRAV = 0.4

vec = pygame.math.Vector2

# klasy
class Dino(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "dino0.png")).convert()  # here's the picture of a player
        self.image.set_colorkey(GREY)  # the background of the dino is light grey, so we should tell python to ignore this colour
        self.rect = self.image.get_rect()
        self.rect.center = (250, 320)  # you can set here the position of the dinosaur on the screen
        self.pos = vec(250, 320)

        self.vel = vec(0, 0)  # velocity
        self.acc = vec(0, 0)  # acceleration

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        self.rect.y -= 1
        if collisions:
            self.vel.y = -20

    def duck(self):
        # duck only if standing on a platform
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        self.rect.y -= 1

    def notduck(self):
        # standup only if standing on a platform
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(player, platforms, False)
        self.rect.y -= 1
        self.rect.center = (250, 320)  # you can set here the position of the dinosaur on the screen
        self.pos = vec(250, 320)

    def update(self):
        # we let him move right and left when we press left and right keys
        self.acc = vec(0, PLAYER_GRAV)

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += (self.vel.y * 0.5 * PLAYER_FRICTION)
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH - 30:
            self.pos.x = WIDTH - 30
        if self.pos.x < 0 + 30:
            self.pos.x = 0 + 30

        self.pos.x = int(round(self.pos.x, 0))
        self.pos.y = int(round(self.pos.y, 0))

        self.rect.midbottom = self.pos

        # CHANGING PLAYER IMAGE
        if dinoCurrentImage == 0:
            self.image = pygame.image.load(os.path.join(img_folder, "dino0.png")).convert()
            self.image.set_colorkey(GREY)
        elif dinoCurrentImage == 1:
            self.image = pygame.image.load(os.path.join(img_folder, "dino1.png")).convert()
            self.image.set_colorkey(GREY)
        elif dinoCurrentImage == 2:
            self.image = pygame.image.load(os.path.join(img_folder, "dino2.png")).convert()
            self.image.set_colorkey(GREY)
        elif dinoCurrentImage == 3:
            self.image = pygame.image.load(os.path.join(img_folder, "ducking_dino1.png")).convert()
            self.image.set_colorkey(GREY)
            self.rect.center = (250, 315)  # you can set here the position of the dinosaur on the screen
            self.pos = vec(250, 320)
        elif dinoCurrentImage == 4:
            self.image = pygame.image.load(os.path.join(img_folder, "ducking_dino2.png")).convert()
            self.image.set_colorkey(GREY)
            self.rect.center = (250, 315)  # you can set here the position of the dinosaur on the screen
            self.pos = vec(250, 320)
        elif dinoCurrentImage == 5:
            self.image = pygame.image.load(os.path.join(img_folder, "hedied.png")).convert()
            self.image.set_colorkey(GREY)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class cactus_1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "big_cactus1.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 4, self.y +2, 31, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cactus_2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "big_cactus2.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 5, self.y - 2, 31, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cactus_3(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "big_cactus3.png")).convert()
        self.hitbox = (self.x - 5, self.y - 3, 20, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cactus_small_1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "small_cactus1.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 6, self.y + 8, 15, 70)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cactus_small_2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "small_cactus2.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 6, self.y - 3, 18, 70)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cactus_small_3(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "small_cactus3.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 3, self.y +10, 12, 35)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))



class cactus_grup_1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "four_cacti1.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 3, self.y +10, 12, 35)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))
class cactus_grup_2(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "four_cacti2.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 3, self.y +10, 12, 35)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))
class cactus_grup_3(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "four_cacti3.png")).convert()
        self.img.set_colorkey(GREY)
        self.hitbox = (self.x - 3, self.y +10, 12, 35)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))

class ptero(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "ptero1.png")).convert()
        self.hitbox = (self.x - 5, self.y - 3, 35, 30)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


# clouds without hitboxes
class cloud(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "cloud.png")).convert()
        self.hitbox = (0, 0, 0, 0)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


class cloud1(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, DS):
        self.img = pygame.image.load(os.path.join(img_folder, "cloud1.png")).convert()
        self.hitbox = (0, 0, 0, 0)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x, self.y))


def redrawWindow():
    for object in objects:
        object.draw(DS)


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

p1 = Platform(0, 320, WIDTH, 40)
player = Dino()

platforms.add(p1)
all_sprites.add(player)
all_sprites.add(p1)

# Game loop
obstacles = []
pygame.time.set_timer(USEREVENT + 2, random.randint(1000, 2000))  # game timer
clouds = []
game_over = False
RUNNING = True
DUCKING = False
pygame.mixer.music.play(-1)

while not game_over:
    score += 0.1

    DS.fill((GREY))
    # keep loop running at the right speed
    CLOCK.tick(FPS)
    # Process input(events)

    for obstacle in obstacles:
        # if polozenie x dinozaura > poczatek hitboxa i < koniec hitboxa:
        #     + jeśli położenie y dinozaura jest > położenie górnej krawędzi hitboxa i < położenie dolnej:
        # Kolizja!!!
        if (player.rect.x + 30) > obstacle.hitbox[0] and (player.rect.x) < obstacle.hitbox[0] + obstacle.hitbox[2]:
            if (player.rect.y + 30) > obstacle.hitbox[1] and (player.rect.y) < obstacle.hitbox[1] + obstacle.hitbox[3]:

                RUNNING = False
                dinoCurrentImage = 5
                die_sound.play(0)
                game_over = True
                if score > high_score:
                    high_score = score

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player.jump()

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==K_DOWN:
                RUNNING = False
                player.duck()
                DUCKING = True
        if event.type==pygame.KEYUP:
            if event.key==K_DOWN:
                DUCKING = False
                player.notduck()
                RUNNING = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                jump_sound.play(0)
                RUNNING = False
                DUCKING = False
        if event.type == pygame.KEYUP:
            if event.key == K_SPACE:
                DUCKING = False
                RUNNING = True

        if event.type == USEREVENT + 2:
            r = random.randrange(0, 12)

            if r == 0:
                obstacles.append(cactus_1(1000, 270, 70, 64))
            elif r == 1:
                obstacles.append(cactus_2(1000, 270, 70, 64))
            elif r == 2:
                obstacles.append(cactus_3(1000, 270, 70, 64))

            elif r == 3:
                obstacles.append(cactus_small_1(1000, 270, 70, 64))
            elif r == 4:
                obstacles.append(cactus_small_2(1000, 270, 70, 64))
            elif r == 5:
                obstacles.append(cactus_small_3(1000, 270, 70, 64))
            elif r == 6:
                obstacles.append(cactus_grup_1(1000, 270, 70, 64))
            elif r == 7:
                obstacles.append(cactus_grup_2(1000, 270, 70, 64))
            elif r == 8:
                obstacles.append(cactus_grup_3(1000, 270, 70, 64))

            # PTEROS ON DIFFERENT HEIGHT
            elif r == 9:
                obstacles.append(ptero(1000, 230, 70, 64))
            elif r == 10:
                obstacles.append(ptero(1000, 240, 70, 64))
            elif r == 11:
                obstacles.append(ptero(1000, 270, 70, 64))


        pygame.time.set_timer(USEREVENT + 2, random.randint(500, 1500))

        if event.type == USEREVENT + 3:
            random_cloud = random.randrange(0, 5)
            # CLOUDS
            if random_cloud == 1:
                clouds.append(cloud(1000, 210, 70, 64))
            elif random_cloud == 2:
                clouds.append(cloud(1000, 180, 70, 64))
            elif random_cloud == 3:
                clouds.append(cloud1(1000, 180, 70, 64))
            elif random_cloud == 4:
                clouds.append(cloud1(1000, 160, 70, 64))
        pygame.time.set_timer(USEREVENT + 3, random.randint(500, 2000))

    # scrolling background
    rel_x = x % background.get_rect().width
    DS.blit(background, (rel_x - background.get_rect().width, 300))
    if rel_x < WIDTH:
        DS.blit(background, (rel_x, 300))
    x -= 3

    # Loops through all obstacles
    for obstacle in obstacles:
        obstacle.draw(DS)
    for obstacle in obstacles:
        obstacle.x -= 3
        if obstacle.x < obstacle.width * -2:
            obstacles.pop(obstacles.index(obstacle))
    #loop for CLOUDS
    for c in clouds:
        c.draw(DS)
    for c in clouds:
        c.x -= 2
        if c.x < c.width * -2:
            clouds.pop(clouds.index(c))
    # Update
    all_sprites.update()

    ground_collisions = pygame.sprite.spritecollide(player, platforms, False)
    if ground_collisions:
        player.pos.y = ground_collisions[0].rect.top
        player.vel.y = 0

    all_sprites.draw(DS)

    if high_score < 10:
        if score < 10:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  0000" + str(round(score)), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  000" + str(round(score)), 20, 800, 10)
        elif score > 100 and score < 130:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 500:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 500 and score < 530:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 1000 and score < 1030:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  0" + str(round(score)), 20, 800, 10)
        else:
            draw_text(DS, "HI 0000" + str(round(high_score)) + "  " + str(round(score)), 20, 800, 10)
    elif high_score < 100:
        if score < 10:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  0000" + str(round(score)), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  000" + str(round(score)), 20, 800, 10)
        elif score > 100 and score < 130:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 500:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 500 and score < 530:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 1000 and score < 1030:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  0" + str(round(score)), 20, 800, 10)
        else:
            draw_text(DS, "HI 000" + str(round(high_score)) + "  " + str(round(score)), 20, 800, 10)
    elif high_score < 1000:
        if score < 10:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  0000" + str(round(score)), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  000" + str(round(score)), 20, 800, 10)
        elif score > 100 and score < 130:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 500:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 500 and score < 530:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 1000 and score < 1030:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  0" + str(round(score)), 20, 800, 10)
        else:
            draw_text(DS, "HI 00" + str(round(high_score)) + "  " + str(round(score)), 20, 800, 10)
    elif high_score < 10000:
        if score < 10:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  0000" + str(round(score)), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  000" + str(round(score)), 20, 800, 10)
        elif score > 100 and score < 130:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 500:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 500 and score < 530:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 1000 and score < 1030:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  0" + str(round(score)), 20, 800, 10)
        else:
            draw_text(DS, "HI 0" + str(round(high_score)) + "  " + str(round(score)), 20, 800, 10)
    else:
        if score < 10:
            draw_text(DS, "HI " + str(round(high_score)) + "  0000" + str(round(score)), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI " + str(round(high_score)) + "  000" + str(round(score)), 20, 800, 10)
        elif score > 100 and score < 130:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 500:
            draw_text(DS, "HI " + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 500 and score < 530:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI " + str(round(high_score)) + "  00" + str(round(score)), 20, 800, 10)
        elif score > 1000 and score < 1030:
            draw_text(DS, "ŚWIETNA  ROBOTA!!", 35, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI " + str(round(high_score)) + "  0" + str(round(score)), 20, 800, 10)
        else:
            draw_text(DS, "HI " + str(round(high_score)) + "  " + str(round(score)), 20, 800, 10)

    if RUNNING == True and DUCKING == False:
        if dinoCurrentImage == 2 or dinoCurrentImage == 3 or dinoCurrentImage == 4:
            dinoCurrentImage = 0
        else:
            dinoCurrentImage += 1

    elif DUCKING == True and RUNNING == False:
        if dinoCurrentImage == 4:
            dinoCurrentImage = 3
        else:
            dinoCurrentImage += 1

    # flip AFTER drawing the display
    pygame.display.flip()

    while game_over:
        show_game_over_screen()
        pygame.mixer.music.stop()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    waiting = False
                    pygame.quit()
                    sys.exit()
                if (event.type == KEYDOWN and event.key == pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    game_over = False
                    score = 0
                    pygame.mixer.music.play(-1)
                    player = Dino()
                    all_sprites = pygame.sprite.Group()
                    platforms = pygame.sprite.Group()
                    p1 = Platform(0, 320, WIDTH, 40)
                    platforms.add(p1)
                    all_sprites.add(player)
                    all_sprites.add(p1)
                    obstacles = []
                    RUNNING = True
                    dinoCurrentImage = 0
pygame.quit()
