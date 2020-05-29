import pygame
import random
import os

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
