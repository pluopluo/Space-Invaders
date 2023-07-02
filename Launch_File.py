import pygame
import os
from pygame.locals import *
from customcolors import *
def show_text(msg, x, y, color, size):
        fontobj= pygame.font.SysFont("freesans", size)
        msgobj = fontobj.render(msg,False,color)
        screen.blit(msgobj,(x, y))
pygame.init()
screen = pygame.display.set_mode((480,480))
clock = pygame.time.Clock()
while True:
    screen.fill(black)

    ## displaying the space invaders logo 
    Space_Invaders_Logo_Image = pygame.image.load('Space')

    ## drawing the boxes for the space invaders 1 and the space invaders 2
    rect_1 = pygame.draw.rect(screen,yellow,(150,200,100,50))
    rect_2 = pygame.draw.rect(screen,yellow,(150,300,100,50))

    show_text('Space Invaders (Original)',150,200,black,10)
    show_text('Space Invaders 2',150,300,black,10)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            ## checking if the mouse button is clicked at the right area
            if 150 < event.pos[0] < 250 and 200 < event.pos[1] < 250:
                 os.system('C:/Users/pluo0/AppData/Local/Programs/Python/Python311/python.exe "c:/Users/pluo0/OneDrive/Desktop/Space-Invaders/Code - Space Invaders (Original)')
            elif 150 < event.pos[0] < 250 and 300 < event.pos[1] < 350:
                 print('here')
                 os.system('C:/Users/pluo0/AppData/Local/Programs/Python/Python311/python.exe "c:/Users/pluo0/OneDrive/Desktop/Space-Invaders/Code - Space Invaders 2')
                 
    clock.tick(60)
    pygame.display.update()

