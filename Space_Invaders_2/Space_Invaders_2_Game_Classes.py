## setting up pygame
import pygame

## main class
class Game_Element:
    Basic_Sound_Url = 'Sounds\\'
    Basic_Url = 'Images\\'
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos

class Words_And_Phrases(Game_Element):
    ## uploading all the character names
    Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                            'O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,
                            3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip','period']
    
    ## uploading all the character images, transforming it, and storing it in a dictionary with respective value
    Character_Dictionary = {}
    for character_name in Character_Name_List:

        ## loading the image, transforming it, then storing it
        img = pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg')
        img = pygame.transform.scale(img,(10,14))
        Character_Dictionary[character_name] = img
        
    def __init__(self,xpos,ypos,phrase):

        ## setting up the xpos, ypos and phrase
        super().__init__(xpos,ypos)
        self.phrase = phrase

    def Draw(self,delay=0):

        ## setting up the counter spacing used for drawing 
        Counter_Spacing = 0

        ## iteration process
        for character in self.phrase:

            ## checking if the player decides to skip
            if Player_Selected == True:
                if Flag_Skip == True or Flag_Skip == 'stage_2':
                    if Flag_Skip == True:
                        Fill_Black()
                    break 
            
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
            elif character == '.':
                character = 'period'
            
            ## checking if the character is a string number and changing it to an integar
            string_number_list = ['0','1','2','3','4','5','6','7','8','9']
            if character in string_number_list:
                character = int(character)
            
            ## drawing the letter and increasing the counter spacing
            screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
            Counter_Spacing = Counter_Spacing + 15

            ## pausing if there is a delay
            if delay != 0:
                pygame.display.update()
                Pause(delay/60)

class Alien(Game_Element):                                                                                                                                                                                 
    ## movement
    Speed = 5
    Timer = 20
    Flag_Collide_Side = None
    Flag_Down_Step = False
    
    ## counters
    Counter_Background_Sound = 1

    ## animation
    Current_Animation = 0
    
    ## setting up the letter interaction images from the start screen
    Letter_Flip_Image_List = []

    ## loading and transforming the images then adding it to the list
    for image_number in range(1,5):
        img = pygame.image.load(Game_Element.Basic_Url+'Alien Letter Flip\Interaction '+str(image_number)+'.jpeg')
        img = pygame.transform.scale(img,(32,15))
        Letter_Flip_Image_List.append(img)
    
    ## setting up the alien images
    Image_List = []

    for alien_size in [1,2,3,4,5]:
        alien_color_list = []
        for alien_color in ['White','Green']:
            alien_type_list = []
            for alien_type in range(1,4):
                alien_animation_list = []
                for animation_frame in range(1,3):

                    ## loading the image and deciding the scale factor
                    img = pygame.image.load(Game_Element.Basic_Url+'Alien\\'+str(alien_color)+' '+str(alien_type)+' '+str(animation_frame)+'.jpeg')
                    alien_scale_factor = 2**(alien_size - 1)

                    ## deciding the length of the aliens depending on it's type
                    if alien_type == 3:
                        alien_length = 15
                    else:
                        alien_length = 20

                    ## transforming the image
                    img = pygame.transform.scale(img,(alien_length*alien_scale_factor,15*alien_scale_factor))

                    ## storing the images in lists
                    alien_animation_list.append(img)
                alien_type_list.append(alien_animation_list)
            alien_color_list.append(alien_type_list)
        Image_List.append(alien_color_list)

    def __init__(self,xpos,ypos,type,size):
        super().__init__(xpos,ypos)
        self.type = type
        self.size = size

        ## setting up the scale factor 
        self.scale_factor = 2**(self.size - 1)

        ## setting the health based on it's scale factor
        self.health = self.scale_factor

        ## deciding it's length and width
        if self.type == 3:
            self.length = 15
            self.height = 15
        else:
            self.length = 20
            self.height = 15
        
        ## transforming the length and height based on the scale factor
        self.length = self.length*self.scale_factor
        self.height = self.height*self.scale_factor

    def Move_Alien(self,start_alien = False):
        self.xpos = self.xpos + self.Speed

        ## checking if the alien is a start alien from the parameters
        if start_alien == True:
            ## changing the alien's animation
            if self.Current_Animation == 0:
                self.Current_Animation = 1
            elif self.Current_Animation == 1:
                self.Current_Animation = 0

        ## checking if the alien hits the edge
        if self.xpos + self.length >= 440:
            Alien.Flag_Collide_Side = 'right'
        elif self.xpos <= 35:
            Alien.Flag_Collide_Side = 'left'
    
    def Change_Animation():
        ## changing the alien's animation
        if Alien.Current_Animation == 0:
            Alien.Current_Animation = 1
        elif Alien.Current_Animation == 1:
            Alien.Current_Animation = 0

    def Move_Down(self):
        ## nonlocalizing the flag game variable
        nonlocal Flag_Game_Level

        ## changing the aliens' ypos
        self.ypos = self.ypos + 15

        ## changing the aliens' speed based on the collide side
        if Alien.Flag_Collide_Side == 'left':
            Alien.Speed = 5
        elif Alien.Flag_Collide_Side == 'right':
            Alien.Speed = -5
        Alien.Flag_Collide_Side = None

    def Check(self):
        ## checking if the aliens reach the Barrier
        if self.ypos + self.height > 330 and self.ypos < 370:
            if self.xpos + self.length > 48 and self.xpos < 108:
                Alien_Barrier_Collision(self,Barrier1)
            elif self.xpos + self.length > 156 and self.xpos < 216:
                Alien_Barrier_Collision(self,Barrier2)
            elif self.xpos + self.length > 264 and self.xpos < 324:
                Alien_Barrier_Collision(self,Barrier3)
            elif self.xpos + self.length > 372 and self.xpos < 432:
                Alien_Barrier_Collision(self,Barrier4)

        # checking if the aliens hit the invasion line or invade
        if self.ypos + self.height >= 435:
            nonlocal Flag_Gameover
            Flag_Gameover = True

    def Shoot(self):
        ## aliens shooting a bullet at player 1
        if player_1 != None:
            if self.xpos + self.length > player_1.xpos and player_1.xpos + player_1.length > self.xpos:
                if random.randint(1,70) == 1:
                    alien_bullets.append(Alien_Bullet(self.xpos + self.length/2,self.ypos + self.height))
        
        # aliens shooting a bullet at player 2
        if player_2 != None:
            if self.xpos + self.length > player_2.xpos and player_2.xpos + player_2.length > self.xpos:
                if random.randint(1,70) == 1:
                    alien_bullets.append(Alien_Bullet(self.xpos + self.length/2,self.ypos + self.height))

    def Split(self):
        ## removing the alien from the screen
        aliens.remove(self)

        ## checking if the alien should explode
        if self.size == 1:
                
                ## adding the explosion to the explosion list
                Alien_Explosion_List.append(Alien_Explosion(self.xpos,self.ypos))
        
        ## checking if the size is greater then 1 and making it split
        elif self.size > 1:
                
                ## adding more aliens to the screen
                for row in range(0,2):
                    for column in range(0,2):
                        aliens.append(Alien(self.xpos + row*self.length/2,self.ypos + column*self.height/2,self.type,self.size - 1))

    def Copy_Alien(self):
        ## globalizing variables
        nonlocal aliens

        ## checking if the alien is within the right ypos
        if self.ypos == 95:

            ## generating the new aliens 
            aliens.append(Alien(self.xpos,self.ypos - 15,3,self.size))

    def Draw(self,color='white'):
        ## drawing the alien based on the color selected
        if color == 'white':
            return screen.blit(Alien.Image_List[self.size - 1][0][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))
        elif color == 'green':
            return screen.blit(Alien.Image_List[self.size - 1][1][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))
        elif color == 'red':
            return screen.blit(Alien.Image_List[self.size - 1][2][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))

    def Draw_Letter_Take(self):
        return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation],(self.xpos - 8,self.ypos))
    def Draw_Letter_Place(self):
        return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation + 2],(self.xpos - 8,self.ypos))

class Player(Game_Element):
    ## setting up the shoot sound
    Shoot_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player shoot sound.wav')

    ## setting up the flag variables
    Flag_Struck = False
    Flag_Movement_Direction = None

    ## setting up the counter variables
    Shoot_Iteration_Counter = 0
    Lucky_Shot = False
    
    ## setting up the player's image
    Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player green.jpeg')
    Green_Image = pygame.transform.scale(Img,(30,20))

    Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player blue.jpeg')
    Blue_Image = pygame.transform.scale(Img,(30,20))

    ## setting up the shoot timer
    Shoot_Timer = 0

    def __init__(self,xpos,ypos):
        super().__init__(xpos,ypos)
        self.length = 30
        self.height = 20

    def Move_Player(self):
        ## updating the shoot timer
        if self.Shoot_Timer > 0:
            self.Shoot_Timer = self.Shoot_Timer - 1
        
        if self.Flag_Movement_Direction == 'left':
            self.xpos = self.xpos - 3
        elif self.Flag_Movement_Direction == 'right':
            self.xpos = self.xpos + 3
        if self.xpos > 410:
            self.xpos = 410
        elif self.xpos < 35:
            self.xpos = 35
    
    def Draw(self,color='green'):
        if color == 'green':
            return screen.blit(Player.Green_Image,(self.xpos,self.ypos))
        elif color == 'blue':
            return screen.blit(Player.Blue_Image,(self.xpos,self.ypos))

class Mystery_Ship(Game_Element):
    ## adding the images
    Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship\Mystery Ship Red.jpeg')
    Image = pygame.transform.scale(Img,(32,14))
    
    ## adding the sounds
    Low_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship low sound.wav')
    Sound_Iteration_Counter = 10

    def __init__(self,xpos,ypos):
        super().__init__(xpos,ypos)
        self.length = 32
        self.height = 14

    def Move_Mystery_Ship(self):
        ## moving the mystery ship
        self.xpos = self.xpos - 2
        ## checking if it should be replaced and the sound counter is also fixed
        if self.xpos + self.length < 0:
            self.xpos = 2500
            self.Sound_Iteration_Counter = 10

    def Draw(self):
        return screen.blit(Mystery_Ship.Image,(self.xpos,self.ypos))
        
    def Play_Sound(self):
        ## playing it's sound
        if self.xpos < 480:
            if self.Sound_Iteration_Counter >= 10:
                self.Low_Sound.play()
                self.Sound_Iteration_Counter = 0
            self.Sound_Iteration_Counter = self.Sound_Iteration_Counter + 1
            
class Player_Bullet(Game_Element):
    ## uploading images
    img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet white.jpeg')
    White_Image = pygame.transform.scale(img,(2,16))
    img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet blue.jpeg')
    Blue_Image = pygame.transform.scale(img,(2,16))
    img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet green.jpeg')
    Green_Image = pygame.transform.scale(img,(2,16))

    ## setting up the sound
    Alien_Collide_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'alien shot sound.wav')

    ## setting up the destruction ranges
    Dr = [2,5,4,7]

    def __init__(self,xpos,ypos):
        super().__init__(xpos,ypos)
        self.height = 16
        self.length = 2 

    def Move_Bullet(self):
        self.ypos = self.ypos - 5

    def Check(self):
        ## declaring nonlocals to the bullets and scores
        nonlocal player_1_bullets, player_2_bullets
        nonlocal player_1_score, player_2_score

        ## checking if the player_1_bullets hit the Barriers
        if self.ypos + self.height > 330 and self.ypos < 370:
            if self.xpos + self.length > 48 and self.xpos < 108:
                Bullet_Barrier_Collision(Barrier1,self)
            elif self.xpos + self.length > 156 and self.xpos < 216:
                Bullet_Barrier_Collision(Barrier2,self)
            elif self.xpos + self.length > 264 and self.xpos < 324:
                Bullet_Barrier_Collision(Barrier3,self)
            elif self.xpos + self.length > 372 and self.xpos < 432:
                Bullet_Barrier_Collision(Barrier4,self)

        ## checking if the bullets hit the alien
        if self in player_1_bullets or self in player_2_bullets:
            for alien in aliens:
                if Collide(alien,self) == True:

                    ## playing the alien collide sound
                    Player_Bullet.Alien_Collide_Sound.play()

                    ## subtracting health from the aliens
                    alien.health = alien.health - 1
                    
                    ## checking if the alien's health is equal to zero
                    if alien.health == 0:

                        ## splitting the alien
                        alien.Split()
                    else:
                        ## removing the bullet from the player bullet's list
                        if self in player_1_bullets:
                            player_1_bullets.remove(self)
                        elif self in player_2_bullets:
                            player_2_bullets.remove(self)
                        
                        ## breaking otherwise because the player's score are not updated unless the alien disappears
                        break

                    ## checking how much should be added to the scores based on the alien type
                    increment = 0
                    if alien.type == 2:
                        increment = 1
                    elif alien.type == 1:
                        increment = 2
                    elif alien.type == 3:
                        increment = 3

                    ## updating the player scores and removing the player's bullet
                    if self in player_1_bullets:
                        player_1_bullets.remove(self)
                        player_1_score.phrase[2] = player_1_score.phrase[2] + increment
                    elif self in player_2_bullets:
                        player_2_bullets.remove(self)
                        player_1_score.phrase[2] = player_1_score.phrase[2] + increment

                    ## updating the high score
                    high_score.phrase[2] = high_score.phrase[2] + increment
                    break 

                ## ending the iteration if the bullet is removed
                if self not in player_1_bullets and self not in player_2_bullets:
                    break

        ## checking if the bullet hits the mystery ship
        if self in player_1_bullets:
            if Collide(self,mystery_ship) == True:

                ## checking if the player 1 bullets hits the mystery ship at the 15th shot and making it worth 300 points
                    if player_1.Lucky_Shot == True:
                        if (player_1.Shoot_Iteration_Counter - 23)%15 == 0:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                            player_1_score.phrase[1] = player_1_score.phrase[1] + 3
                            high_score.phrase[1] = high_score.phrase[1] + 3
                        else:
                            player_1.Lucky_Shot = False

                ## checking if otherwise and making it worth 200 points
                    if player_1.Lucky_Shot == False:
                        Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                        player_1_score.phrase[1] = player_1_score.phrase[1] + 2
                        high_score.phrase[1] = high_score.phrase[1] + 2

                ## checking if the player 1 bullet hits the mystery ship on the 23rd shot 
                    if player_1.Shoot_Iteration_Counter == 23:
                        player_1.Lucky_Shot = True

                ## relocating the mystery ship
                    mystery_ship.xpos = 2500

                ## removing the bullet from the bullet list
                    player_1_bullets.remove(self)

                ## playing the mystery ship's explosion sound
                    Mystery_Ship_Explosion.Sound.play()

        elif self in player_2_bullets:
            if Collide(self,mystery_ship) == True:

                ## checking if the player 2's bullets hits the mystery ship at the 15th shot and making it worth 300 points
                    if player_2.Lucky_Shot == True:
                        if (player_2.Shoot_Iteration_Counter - 23)%15 == 0:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                            player_2_score.phrase[1] = player_1_score.phrase[1] + 3
                            high_score.phrase[1] = high_score.phrase[1] + 3
                        else:
                            player_2.Lucky_Shot = False

                ## checking if otherwise and making it worth 200 points
                    if player_2.Lucky_Shot == False:
                        Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                        player_2_score.phrase[1] = player_2_score.phrase[1] + 2
                        high_score.phrase[1] = high_score.phrase[1] + 2
                        
                ## checking if the player 2's bullet hits the mystery ship on the 23rd shot
                    if player_2.Shoot_Iteration_Counter == 23:
                        player_2.Lucky_Shot = True

                ## relocating the mystery ship
                    mystery_ship.xpos = 2500

                ## removing the bullet from the bullet list
                    player_2_bullets.remove(self)

                ## playing the mystery ship's explosion sound
                    Mystery_Ship_Explosion.Sound.play()

        ## checking if the hundreads or thousands place in the scores should be updated
        Update_Score(player_1_score)
        Update_Score(player_2_score)
        Update_Score(high_score)

        ## checking if the player bullet hits the top of the screen
        if self in player_1_bullets or self in player_2_bullets:
            if self.ypos < 0:
                if self in player_1_bullets:
                    player_1_bullets.remove(self)
                elif self in player_2_bullets:
                    player_2_bullets.remove(self)
                Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 6,self.ypos))

    def Draw(self,color='white'):
        if color == 'white':
            return screen.blit(Player_Bullet.White_Image,(self.xpos,self.ypos))
        elif color == 'blue':
            return screen.blit(Player_Bullet.Blue_Image,(self.xpos,self.ypos))
        elif color == 'green':
            return screen.blit(Player_Bullet.Green_Image,(self.xpos,self.ypos))

class Alien_Bullet(Game_Element):
    ## class variables
    Current_Animation = 1
    
    layout_1 = [[2,2,2,2,2,6],
                [2,2,2,6,2,2],
                [2,2,6,2,2,2],
                [6,2,2,2,2,2]]
    layout_2 = [[2,2,4,5,2,4,5],
                [2,2,4,5,2,4,5],
                [5,4,2,5,4,2,2],
                [5,4,2,5,4,2,2]]
    layout_3 = [[2,1,2,3,2,1,2],
                [1,2,3,2,1,2,3],
                [2,3,2,1,2,3,2],
                [3,2,1,2,3,2,1]]
    
    ## uploading all the alien bullet images
    Image_List = []
    for color in ['White','Green']:
        color_list = []
        for image_particle in range(1,7):
            img = pygame.image.load(Game_Element.Basic_Url+'Alien Bullet\\alien bullet '+str(image_particle)+' '+str(color)+'.jpeg')
            img = pygame.transform.scale(img,(6,2))
            color_list.append(img)   
        Image_List.append(color_list)

    def __init__(self,xpos,ypos):
        ## setting up the cordinates and the type 
        self.xpos = xpos
        self.ypos = ypos
        self.type = random.randint(1,3)

        ## setting up the attributes such as the varying lengths, heights, the Barrier destruction range
        if self.type == 1:
            self.length = 6
            self.height = 12
            self.Dr = [2,5,4,7]
        elif self.type == 2:
            self.length = 6
            self.height = 14
            self.Dr = [2,5,4,8]
        elif self.type == 3:
            self.length = 6
            self.height = 14
            self.Dr = [3,5,5,7]
    
    def Move_Alien_Bullet(self):
        ## updating the animation
        self.Current_Animation = self.Current_Animation + 1
        if self.Current_Animation == 4:
            self.Current_Animation = 0
        ## updating the y cordinates
        self.ypos = self.ypos + 3

    def Check(self):
        nonlocal alien_bullets, Bullet_Explosion_List
        alien_bullets_length = len(alien_bullets)
        ## checking if the alien_bullets hit the Barriers
        if self.ypos + self.height > 330 and self.ypos < 370:
            if self.xpos + self.length > 48 and self.xpos < 108:
                Bullet_Barrier_Collision(Barrier1,self)
            elif self.xpos + self.length > 156 and self.xpos < 216:
                Bullet_Barrier_Collision(Barrier2,self)
            elif self.xpos + self.length > 264 and self.xpos < 324:
                Bullet_Barrier_Collision(Barrier3,self)
            elif self.xpos + self.length > 372 and self.xpos < 432:
                Bullet_Barrier_Collision(Barrier4,self)

        ## checking if the alien_bullets hits the boundary line
        if self.ypos + self.height > 435 and len(alien_bullets) == alien_bullets_length:
            Bullet_Barrier_Collision(alien_invasion_line,self)
            if self in alien_bullets:
                alien_bullets.remove(self)
            Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 3,self.ypos - 4,))

        ## checking if the alien_bullet hit the player bullet
        if len(alien_bullets) == alien_bullets_length:
            for bullet in player_1_bullets:
                if self.xpos + self.length > bullet.xpos and bullet.xpos + bullet.length > self.xpos and self.ypos + self.height > bullet.ypos and bullet.ypos + bullet.height > self.ypos:
                    player_1_bullets.remove(bullet)
                    Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                    if self.type == 1:
                        if random.randint(1,2) == 1:
                            alien_bullets.remove(self)
                    elif self.type == 2:
                        if random.randint(1,3) == 1:
                            alien_bullets.remove(self)
                    break

        if len(alien_bullets) == alien_bullets_length:
            for bullet in player_2_bullets:
                if Collide(self,bullet) == True:
                    player_2_bullets.remove(bullet)
                    Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                    if self.type == 1:
                        if random.randint(1,2) == 1:
                            alien_bullets.remove(self)
                    elif self.type == 2:
                        if random.randint(1,3) == 1:
                            alien_bullets.remove(self)
                    break

        # ## checking if the alien bullet hits the player
        if len(alien_bullets) == alien_bullets_length:
            if player_1 != None:
                if Collide(self,player_1) == True:
                    alien_bullets.remove(self)
                    player_1.Flag_Struck = True

        if len(alien_bullets) == alien_bullets_length:
            if player_2 != None:
                if Collide(self,player_2) == True:
                    alien_bullets.remove(self)
                    player_2.Flag_Struck = True

    def Draw(self):
        ## drawing the alien bullet
        counter_xpos = 0

        ## checking what type it is and drawing the right images
        if self.type == 1:
            for image_particle in Alien_Bullet.layout_1[self.Current_Animation]:
                if self.ypos + 2 > 330:
                    screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                else:
                    screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                counter_xpos = counter_xpos + 2

        if self.type == 2:
            for image_particle in Alien_Bullet.layout_2[self.Current_Animation]:
                if self.ypos + 2 > 330:
                    screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                else:
                    screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                counter_xpos = counter_xpos + 2

        if self.type == 3:
            for image_particle in Alien_Bullet.layout_3[self.Current_Animation]:
                if self.ypos + 2 > 330:
                    screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                else:
                    screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                counter_xpos = counter_xpos + 2

class Barrier(Game_Element):
    ## setting up the images according to this
    img = pygame.image.load(Game_Element.Basic_Url+'Barrier\\barrier particle.jpeg')
    green_image = pygame.transform.scale(img,(2,2))
    def __init__(self,xpos,ypos):
        super().__init__(xpos,ypos)
        self.length = 2
        self.height = 2
    def Draw(self):
        return screen.blit(Barrier.green_image,(self.xpos,self.ypos))

## setting up the scinario classes
class Alien_Explosion(Game_Element):
    ## setting up the image
    Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion white.jpeg')
    White_Image = pygame.transform.scale(Img,(20,13))
    Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion green.jpeg')
    Green_Image = pygame.transform.scale(Img,(20,13))

    ## setting up the Existing_Timer
    Existing_Timer = 10

    def Update_Timer(self):
        ## removing the explosion when the timer reaches zero
        self.Existing_Timer = self.Existing_Timer - 1
        if self.Existing_Timer == 0:
            nonlocal Alien_Explosion_List
            Alien_Explosion_List.remove(self)

    def Draw(self):
        if self.ypos + 13 > 330:
            screen.blit(Alien_Explosion.Green_Image,(self.xpos,self.ypos))
        else: 
            screen.blit(Alien_Explosion.White_Image,(self.xpos,self.ypos))

class Mystery_Ship_Explosion(Alien_Explosion):
    ## uploading the images
    Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship explosion red.jpeg')
    Explosion_Image = pygame.transform.scale(Img,(42,16))
    Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
    Score_200_Image = pygame.transform.scale(Img,(40,14)) 
    Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
    Score_300_Image = pygame.transform.scale(Img,(40,14)) 

    ## setting up the existing timer
    Existing_Timer = 20

    ## setting up the sound
    Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship high sound.wav')

    def __init__(self,xpos,ypos,points=200):
        super().__init__(xpos,ypos)
        self.points = points

    def Update_Timer(self):
        ## removing the explosion when the timer reaches zero
        self.Existing_Timer = self.Existing_Timer - 1
        if self.Existing_Timer == 0:
            nonlocal Mystery_Ship_Explosion_List
            Mystery_Ship_Explosion_List.remove(self)

    def Draw(self):
        if self.Existing_Timer > 10:
            screen.blit(Mystery_Ship_Explosion.Explosion_Image,(self.xpos - 4,self.ypos))
        else:
            if self.points == 300:
                screen.blit(Mystery_Ship_Explosion.Score_300_Image,(self.xpos - 4,self.ypos))
            else:
                screen.blit(Mystery_Ship_Explosion.Score_200_Image,(self.xpos - 4,self.ypos))

class Bullet_Explosion(Game_Element):
    Img = pygame.image.load(Game_Element.Basic_Url+'Bullet Explosions\\bullet and bullet explosion.jpeg')
    Image = pygame.transform.scale(Img,(12,16))
    Explosion_Timer = 4
    def Draw(self):
        return screen.blit(Bullet_Explosion.Image,(self.xpos,self.ypos))

class Player_Explosion(Game_Element):
    ## uploading the sound
    Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player explosion sound.wav')

    ## uploading the player explosion images
    Image_List = []
    for image_number in range(1,4):
        img = pygame.image.load(Game_Element.Basic_Url+'Player Explosion\player explosion '+str(image_number)+'.jpeg')
        Image_List.append(pygame.transform.scale(img,(40,20)))

    def __init__(self,xpos,ypos,length,height):
        super().__init__(xpos,ypos)
        self.length = length
        self.height = height

    def Draw(self,image_number):
        if image_number == 1:
            screen.blit(Player_Explosion.Image_List[0],(self.xpos,self.ypos))
        elif image_number == 2:
            screen.blit(Player_Explosion.Image_List[1],(self.xpos,self.ypos))
        elif image_number == 3:
            screen.blit(Player_Explosion.Image_List[2],(self.xpos,self.ypos))