print("Hello world!")
import pygame
import random
import os

WIDTH=800
HEIGHT=500
FPS=30

#define colors
WHITE=(255,255,255)
GREY=(247,247,247)

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
        self.y_speed=0

#initialize pygame and create game window
pygame.init()
screen=pygame.display.set_mode((WIDTH, HEIGHT)) #it sets the screen
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

    #Update
    all_sprites.update()

    #Draw/render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    #flip AFTER drawing the display
    pygame.display.flip()

pygame.quit()

