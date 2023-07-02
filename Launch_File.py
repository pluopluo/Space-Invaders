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

class Words_And_Phrases():
    ## uploading all the character names
    Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                            'O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,
                            3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip']
        
    ## uploading all the character images, transforming it, and storing it in a dictionary with respective value
    Character_Dictionary = {}
    for character_name in Character_Name_List:

        ## loading the image, transforming it, then storing it
        img = pygame.image.load('Images\letters\\'+str(character_name)+'.jpeg')
        img = pygame.transform.scale(img,(10,14))
        Character_Dictionary[character_name] = img
            
    def __init__(self,xpos,ypos,phrase):

        ## setting up the xpos, ypos and phrase
        self.xpos = xpos
        self.ypos = ypos
        self.phrase = phrase

    def Draw(self):

        ## setting up the counter spacing used for drawing 
        Counter_Spacing = 0

        ## iteration process
        for character in self.phrase:
                
            ## checking if the character is a symbol and changing it to words
            if character == '<':
                character = 'left'
            elif character == '>':
                character = 'right'
            elif character == '=':
                character = 'equal'
            elif character == '*':
                character = 'asterisk'
            elif character == '?':
                character = 'question_mark'
            elif character == '-':
                character = 'dash'
            elif character == ' ':
                character = 'space'
                
            ## checking if the character is a string number and changing it to an integar
            string_number_list = ['0','1','2','3','4','5','6','7','8','9']
            if character in string_number_list:
                character = int(character)
                
            ## drawing the letter and increasing the counter spacing
            screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
            Counter_Spacing = Counter_Spacing + 15

## setting up the asterisk 
asterisk = Words_And_Phrases(90,225,'*')

## setting up the flag game mode
Flag_Game_Mode == 'One_Player'
while True:
    screen.fill(black)

    ## displaying the space invaders logo 
    Space_Invaders_Logo_Image = pygame.image.load('Images/Space Invaders Logo.jpeg')
    screen.blit(Space_Invaders_Logo_Image,(120,100))

    def middle(text):
        a = 480 - 15*len(text)
        print(a/2)

    ## drawing the text for the Space Invaders 1 and the space invaders 2
    Space_Invaders_Original_Message = Words_And_Phrases(120,225,'SPACE INVADERS')
    Space_Invaders_Original_Message.Draw()

    ## drawing the text for the Space Invaders 2
    Space_Invaders_2_Message = Words_And_Phrases(120,265,'SPACE INVADERS 2')
    Space_Invaders_2_Message.Draw()

    ## drawing the asterisk
    asterisk.Draw()
    middle(Space_Invaders_Original_Message.phrase)
    middle(Space_Invaders_2_Message.phrase)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                ## changing the asterisk's position:
                asterisk.ypos = 265
            
            elif event.key == K_UP:
                ## changing the asterisk's position
                asterisk.ypos = 225

            elif event.key == K_RETURN:
                ## checking if the mouse button is clicked at the right area
                if 150 < event.pos[0] < 250 and 200 < event.pos[1] < 250:
                    os.system('C:/Users/pluo0/AppData/Local/Programs/Python/Python311/python.exe "c:/Users/pluo0/OneDrive/Desktop/Space Invaders/Code - Space Invaders (Original)')
                elif 150 < event.pos[0] < 250 and 300 < event.pos[1] < 350:
                    os.system('C:/Users/pluo0/AppData/Local/Programs/Python/Python311/python.exe "c:/Users/pluo0/OneDrive/Desktop/Space Invaders/Code - Space Invaders 2')
                 
    clock.tick(60)
    pygame.display.update()

