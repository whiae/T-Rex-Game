import random
import pygame
from pygame.locals import *
import sys
import os
import math
import time

#define display surface
WIDTH=1000
HEIGHT=400
HW=WIDTH/2
HH=HEIGHT/2
AREA=WIDTH*HEIGHT

#define colors
WHITE=(255,255,255)
GREY=(247,247,247)
BLACK = (0,0,0)
GREEN = (0,139,69)
PINK = (255,62,150)

#set up assets folders
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"img")

#initialize pygame and create game window
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((WIDTH, HEIGHT)) #it sets the screen
pygame.display.set_caption("T-Rex Game") #it sets the title of the game window
FPS = 120


background = pygame.image.load(os.path.join(img_folder,"ground.png")).convert()
x = 0


font_name = pygame.font.match_font('Comic Sans MS')

def draw_text(surf, text, size, x, y):
# x i y to lokalizacja tekstu na ekranie
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_game_over_screen():
    draw_text(DS, "G A M E   O V E R", 20, WIDTH/2, HEIGHT/3)
    retry_img = pygame.image.load(os.path.join(img_folder,"retry.png")).convert()
    DS.blit(retry_img, (485, HEIGHT/2))
    pygame.display.flip()


score = 0
high_score = 0


#Player properties
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.12 #negative number, because it should slow us down
PLAYER_GRAV=0.45



vec=pygame.math.Vector2

#klasy
class Dino(pygame.sprite.Sprite):
    #sprite for the Player
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(os.path.join(img_folder,"dino.png")).convert() #here's the picture of a player
        self.image.set_colorkey(GREY) #the background of the dino is light grey, so we should tell python to ignore this colour
        self.rect=self.image.get_rect()
        self.rect.center=(250,320) #you can set here the position of the dinosaur on the screen
        self.pos=vec(250,320)

        self.vel=vec(0,0) #velocity
        self.acc=vec(0,0) #acceleration

    def jump(self):
        #jump only if standing on a platform
        self.rect.y+=1
        collisions=pygame.sprite.spritecollide(player,platforms,False)
        self.rect.y-=1
        if collisions:
            self.vel.y=-20

    def update(self):
        #we let him move right and left when we press left and right keys
        self.acc=vec(0,PLAYER_GRAV)
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.acc.x=-PLAYER_ACC
        if keystate[pygame.K_RIGHT]:
            self.acc.x=PLAYER_ACC

        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += (self.vel.y * 0.5 * PLAYER_FRICTION)
        #poniższe linijki tylko do sprawdzenia wartości zmiennych
        # print(self.acc)
        # print(self.vel)
        # print(PLAYER_FRICTION)
        #equations of motion
        self.vel+=self.acc
        self.pos+=self.vel+0.5*self.acc
        print(self.pos)
        #wrap around the sides of the screen
        if self.pos.x>WIDTH-30:
            self.pos.x=WIDTH-30
        if self.pos.x<0+30:
            self.pos.x=0+30

        self.pos.x=int(round(self.pos.x,0))
        self.pos.y=int(round(self.pos.y,0))
        #poniższe linijki tylko do sprawdzenia wartości zmiennych
        print(self.pos.x)
        print(self.pos.y)

        self.rect.midbottom=self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        # self.image=pygame.image.load(os.path.join(img_folder,"ground.png")).convert()
        # self.image.set_colorkey(GREY)
        self.image=pygame.Surface((w,h))
        self.image.fill(GREY)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class cactus_1(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load(os.path.join(img_folder,"big_cactus1.png")).convert()
        self.hitbox = (self.x-5, self.y-6, 31, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))

    # def hit(self):


class cactus_2(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load(os.path.join(img_folder,"big_cactus2.png")).convert()
        self.hitbox = (self.x-5, self.y-6, 31, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))

class cactus_3(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load(os.path.join(img_folder,"big_cactus1.png")).convert()
        self.hitbox = (self.x-5, self.y-6, 31, 80)
        pygame.draw.rect(DS, GREY, self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))

def redrawWindow():
	for object in objects:
		object.draw(DS)

#here's a group for all the sprites, we can add dino, cacti and other stuff here
#you can change it if you want :P
all_sprites=pygame.sprite.Group()
platforms=pygame.sprite.Group()

p1=Platform(0,320,WIDTH,40)
player=Dino([320,250])

platforms.add(p1)
all_sprites.add(player)
all_sprites.add(p1)

#sound function and files
def create_sound(name):
    fullname = "snd/" + name     # path + name of the sound file
    sound = pygame.mixer.Sound(fullname)
    return sound

music = create_sound('music.wav')
music.set_volume(0.05)
jump_sound = create_sound('jump.wav')
die_sound = create_sound('die.wav')
checkPoint_sound = create_sound('checkPoint.wav')

# Game loop
obstacles=[]
pygame.time.set_timer(USEREVENT+2, random.randint(1000, 3500)) #game timer

game_over = False


while not game_over:
    score += 1

    DS.fill((GREY))
    #keep loop running at the right speed
    CLOCK.tick(FPS)
    #Process input(events)

    for obstacle in obstacles:
        # if położenie x dinozaura > poczatek hitboxa i < koniec hitboxa:
        #     + jeśli położenie y dinozaura jest > położenie górnej krawędzi hitboxa i < położenie dolnej:
        if (player.rect.x + 23) > obstacle.hitbox[0] and (player.rect.x) < obstacle.hitbox[0] + obstacle.hitbox[2]:
            if (player.rect.y + 24) > obstacle.hitbox[1] and (player.rect.y) < obstacle.hitbox[1] + obstacle.hitbox[3]:
                print("GAME OVER")
                game_over = True
                if score > high_score:
                    high_score = score


    for event in pygame.event.get():
        #check for closing window
        if event.type==pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.jump()

        if event.type == USEREVENT+2:
            r = random.randrange(0,3)
            if r == 0:
                obstacles.append(cactus_1(1000, 270, 70, 64))
            elif r == 1:
                obstacles.append(cactus_2(1000, 270, 70, 64))
            elif r == 2:
                obstacles.append(cactus_3(1000, 270, 70, 64))
        pygame.time.set_timer(USEREVENT+2, random.randint(1000, 3500))

    #scrolling background
    rel_x = x % background.get_rect().width
    DS.blit(background, (rel_x - background.get_rect().width, 300))
    if rel_x < WIDTH:
         DS.blit(background, (rel_x, 300))
    x -= 1.5

    # Loops through all obstacles
    for obstacle in obstacles:
        obstacle.draw(DS)
    for obstacle in obstacles:
        obstacle.x -= 2
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))

    #Update
    all_sprites.update()

    ground_collisions=pygame.sprite.spritecollide(player,platforms,False)
    if ground_collisions:
        player.pos.y=ground_collisions[0].rect.top
        player.vel.y=0

    # pygame.display.update() #nie wiem czy ta linijka jest potrzebna, bo jak ją zostawiam to dinozaur miga; zostawię ją tu na wszelki wypadek, ale jako komentarz
    all_sprites.draw(DS)

    if high_score < 10:
        if score < 10:
            draw_text(DS, "HI 0000" + str(high_score) + "  0000" + str(score), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 0000" + str(high_score) + "  000" + str(score), 20, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 0000" + str(high_score) + "  00" + str(score), 20, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 0000" + str(high_score) + "  0" + str(score), 20, 800, 10)
        else:
            draw_text(DS, "HI 0000" + str(high_score) + "  " + str(score), 20, 800, 10)
    elif high_score < 100:
        if score < 10:
            draw_text(DS, "HI 000" + str(high_score) + "  0000" + str(score), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 000" + str(high_score) + "  000" + str(score), 20, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 000" + str(high_score) + "  00" + str(score), 20, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 000" + str(high_score) + "  0" + str(score), 20, 800, 10)
        else:
            draw_text(DS, "HI 000" + str(high_score) + "  " + str(score), 20, 800, 10)
    elif high_score < 1000:
        if score < 10:
            draw_text(DS, "HI 00" + str(high_score) + "  0000" + str(score), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 00" + str(high_score) + "  000" + str(score), 20, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 00" + str(high_score) + "  00" + str(score), 20, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 00" + str(high_score) + "  0" + str(score), 20, 800, 10)
        else:
            draw_text(DS, "HI 00" + str(high_score) + "  " + str(score), 20, 800, 10)
    elif high_score < 10000:
        if score < 10:
            draw_text(DS, "HI 0" + str(high_score) + "  0000" + str(score), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI 0" + str(high_score) + "  000" + str(score), 20, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI 0" + str(high_score) + "  00" + str(score), 20, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI 0" + str(high_score) + "  0" + str(score), 20, 800, 10)
        else:
            draw_text(DS, "HI 0" + str(high_score) + "  " + str(score), 20, 800, 10)
    else:
        if score < 10:
            draw_text(DS, "HI " + str(high_score) + "  0000" + str(score), 20, 800, 10)
        elif score < 100:
            draw_text(DS, "HI " + str(high_score) + "  000" + str(score), 20, 800, 10)
        elif score < 1000:
            draw_text(DS, "HI " + str(high_score) + "  00" + str(score), 20, 800, 10)
        elif score < 10000:
            draw_text(DS, "HI " + str(high_score) + "  0" + str(score), 20, 800, 10)
        else:
            draw_text(DS, "HI " + str(high_score) + "  " + str(score), 20, 800, 10)

    #flip AFTER drawing the display
    pygame.display.flip()

    while game_over:
            show_game_over_screen()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        waiting = False
                        pygame.quit()
                        sys.exit()
                if (event.type == KEYDOWN and event.key == K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    game_over = False
                    score = 0
                    player=Dino([320,250])
                    all_sprites=pygame.sprite.Group()
                    platforms=pygame.sprite.Group()
                    p1=Platform(0,320,WIDTH,40)
                    platforms.add(p1)
                    all_sprites.add(player)
                    all_sprites.add(p1)
                    obstacles=[]

pygame.quit()
