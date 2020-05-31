import random
import pygame
from pygame.locals import *
import sys
import os
import math

# define display surface
W, H = 800, 600
HW, HH = W / 2, H / 2
AREA = W * H


os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

# setup pygame
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("t-rex")
FPS = 120

bkgd = pygame.image.load("img/ground.png").convert()
x = 0

#player
playerimg = pygame.image.load('img/dino.png')
playerx = 0
playery = 270

def player(x,y):
    DS.blit(playerimg, (x,y))

#cactus

class cactus_1(object):

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load("img/big_cactus2.png")
        self.hitbox = (self.x + 2, self.y + 2, self.width - 20, self.height - 5)
        pygame.draw.rect(DS, (255,0,0), self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))
class cactus_2():

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load("img/big_cactus3.png")
        self.hitbox = (self.x + 2, self.y + 2, self.width - 20, self.height - 5)
        pygame.draw.rect(DS, (255,0,0), self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))

class cactus_3():

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,DS):
        self.img = pygame.image.load("img/big_cactus1.png")
        self.hitbox = (self.x + 2, self.y + 2, self.width - 20, self.height - 5)
        pygame.draw.rect(DS, (255,0,0), self.hitbox, 2)
        DS.blit(self.img, (self.x,self.y))


def redrawWindow():
	for object in objects:
		object.draw(DS)

obstacles = []
#timer which creates first 
pygame.time.set_timer(USEREVENT+2, random.randint(1000, 3500))
while True:
   #events
    DS.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == USEREVENT+2:
            r = random.randrange(0,3)
            if r == 0:
                obstacles.append(cactus_1(800, 270, 70, 64))
            elif r == 1:
                obstacles.append(cactus_2(800, 270, 70, 64))
            elif r == 2:
                obstacles.append(cactus_3(800, 270, 70, 64))
        pygame.time.set_timer(USEREVENT+2, random.randint(1000, 3500))
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    #scrolling background
    rel_x = x % bkgd.get_rect().width
    DS.blit(bkgd, (rel_x - bkgd.get_rect().width, 300))
    if rel_x < W:
         DS.blit(bkgd, (rel_x, 300))
    x -= 1.5


    # Loops through all obstacles
    for obstacle in obstacles:
        obstacle.draw(DS)
    for obstacle in obstacles:
        obstacle.x -= 1.5
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))
	#drawing player
    player(playerx, playery)

    pygame.display.update()
    CLOCK.tick(FPS)

WIDTH=800
HEIGHT=500

FPS=60
TITLE="T-Rex Game"

#Player properties
PLAYER_ACC=0.5
PLAYER_FRICTION=-0.12 #negative number, because it should slow us down
PLAYER_GRAV=0.8

#define colors
WHITE=(255,255,255)
GREY=(247,247,247)


vec=pygame.math.Vector2

#set up assets folders
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"img")

#klasa gracz - nasz dinozaur
class Dino(pygame.sprite.Sprite):
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(os.path.join(img_folder,"dino.png")).convert() #here's the picture of a player
        self.image.set_colorkey(GREY) #the background of the dino is light grey, so we should tell python to ignore this colour
        self.rect=self.image.get_rect()
        self.rect.center=(WIDTH/3,HEIGHT/(4/3)) #you can set here the position of the dinosaur on the screen

        self.pos=vec(WIDTH/3,HEIGHT/(4/3))
        self.vel=vec(0,0) #velocity
        self.acc=vec(0,0) #acceleration

    def jump(self):
        #jump only if standing on a platform
        self.rect.x+=1
        collisions=pygame.sprite.spritecollide(player,platforms,False)
        self.rect.x-=1
        if collisions:
            self.vel.y=-25

    def update(self):
        #we let him move right and left when we press left and right keys
        self.acc=vec(0,PLAYER_GRAV)
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.acc.x=-PLAYER_ACC
        if keystate[pygame.K_RIGHT]:
            self.acc.x=PLAYER_ACC

        #apply friction
        self.acc+=self.vel * PLAYER_FRICTION
        #equations of motion
        self.vel+=self.acc
        self.pos+=self.vel+0.5*self.acc
        #wrap around the sides of the screen
        if self.pos.x>WIDTH-30:
            self.pos.x=WIDTH-30
        if self.pos.x<0+30:
            self.pos.x=0+30

        self.rect.midbottom=self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        # self.image=pygame.image.load(os.path.join(img_folder,"ground.png")).convert()
        # self.image.set_colorkey(GREY)
        self.image=pygame.Surface((w,h))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


#initialize pygame and create game window
pygame.init()
screen=pygame.display.set_mode((WIDTH, HEIGHT)) #it sets the screen
pygame.display.set_caption(TITLE) #it sets the title of the game window
clock=pygame.time.Clock()


#here's a group for all the sprites, we can add dino, cacti and other stuff here
#you can change it if you want :P
all_sprites=pygame.sprite.Group()
platforms=pygame.sprite.Group()
p1=Platform(0,400,WIDTH,40)
player=Dino()
all_sprites.add(player)
platforms.add(p1)
all_sprites.add(p1)


pygame.display.set_caption("T-Rex Game") #it sets the title of the game window
clock=pygame.time.Clock()

#here's a group for all the sprites, we can add dino, cacti and other stuff here
#you can change it if you want :P
all_sprites=pygame.sprite.Group()
player=Dino()
all_sprites.add(player)

# Game loop
running=True
while running:
    #keep loop running at the right speed
    clock.tick(FPS)
    #Process input(events)
    for event in pygame.event.get():
        #check for closing window
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                player.jump()


    #Update
    all_sprites.update()


    ground_collisions=pygame.sprite.spritecollide(player,platforms,False)
    if ground_collisions:
        player.pos.y=ground_collisions[0].rect.top
        player.vel.y=0


    #Draw/render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    #flip AFTER drawing the display
    pygame.display.flip()

pygame.quit()

