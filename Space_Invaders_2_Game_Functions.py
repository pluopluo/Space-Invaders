## space invaders game functions

def Close_Or_Skip():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        ## skipping if the enter key is pressed
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:              
                nonlocal Flag_Skip
                if Flag_Skip == False:
                    Flag_Skip = True

def Pause(time):
    num_of_time_units = int(time*60)
    for time_unit in range(0,num_of_time_units):
        ## checking if the player has pressed skip when the screen pauses
        Close_Or_Skip()
    if Flag_Skip == True or Flag_Skip == 'stage_2':
            if Flag_Skip == True:
                Fill_Black()
            break
        clock.tick(60)

def Collide(object_1,object_2):
    if object_1.xpos + object_1.length > object_2.xpos and object_2.xpos + object_2.length > object_1.xpos:
        if object_1.ypos + object_1.height > object_2.ypos and object_2.ypos + object_2.height > object_1.ypos:
            return True
        
def Alien_Barrier_Collision(alien,Barrier):
    Barrier_Iteration_Counter = 0
    Barrier_Struck = False

    ## iterating through the barriers
    while True:
        if Barrier_Iteration_Counter == len(Barrier):
            break

        ## checking if a barrier block hit the alien
        if alien.xpos + alien.length >= Barrier[Barrier_Iteration_Counter].xpos and alien.xpos <= Barrier[Barrier_Iteration_Counter].xpos + Barrier[Barrier_Iteration_Counter].length:
            if alien.ypos + alien.height >= Barrier[Barrier_Iteration_Counter].ypos:
                Barrier_Struck = True
        
        ## destroying the barrier block
        if Barrier_Struck == True:
            Barrier.pop(Barrier_Iteration_Counter)
            Barrier_Struck = False
        else:
            ## updating the iteration counter only if the barrier isn't destroyed
            Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1

def Bullet_Barrier_Collision(Barrier,bullet):
    ## declaring nonlocals to the bullet lists and the bullet explosion list
    nonlocal player_1_bullets, player_2_bullets, alien_bullets, Bullet_Explosion_List

    ## checking what type of bullet it is and what iteration should be performed ont he Barrier
    if bullet in alien_bullets:
        Barrier_Iteration = [0,len(Barrier),1]
        
    elif bullet in player_1_bullets or bullet in player_2_bullets:
        Barrier_Iteration = [len(Barrier) - 1,-1,-1]
        
    ## checking the Barrier and if the divisor is supposed to be 2
    if Barrier == alien_invasion_line:
        divisor = 2
    else:
        divisor = 1

    Target_Barrier = None
    ## checking the specific particle the bullet hits
    for i in range(Barrier_Iteration[0],Barrier_Iteration[1],Barrier_Iteration[2]):
        if Collide(bullet,Barrier[i]) == True:
            Target_Barrier = Barrier[i]
            Barrier_Iteration_Counter = 0
            Barrier_Struck = False
            while True:
                # breaking the bullet and the while loop
                if Barrier_Iteration_Counter >= len(Barrier):
                    if bullet in alien_bullets:
                        alien_bullets.remove(bullet)
                    if bullet in player_1_bullets:
                        player_1_bullets.remove(bullet)
                    if bullet in player_2_bullets:
                        player_2_bullets.remove(bullet)
                    break
            
                ## checking if the xpos is correct
                if Barrier[Barrier_Iteration_Counter].xpos%(divisor*2) == 0:
                    ## checking if the Barrier particle is in close range of the area hit by the bullet
                    if Target_Barrier.xpos - bullet.Dr[0]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.length + bullet.Dr[0]:
                        if Target_Barrier.ypos - bullet.Dr[1]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[1]*2:
                            Barrier_Struck = True
                        
                    ## checking if the Barrier particle is in far range of the area struck by the bullet
                    if Target_Barrier.xpos - bullet.Dr[2]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.height + bullet.Dr[2]*2:
                        if Target_Barrier.ypos - bullet.Dr[3]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[3]*2:
                            # deciding how far it is and the chance of the Barrier being destroyed
                            y_distance = abs(Target_Barrier.ypos - Barrier[Barrier_Iteration_Counter].ypos) + 1
                            x_distance = abs(Target_Barrier.xpos - Barrier[Barrier_Iteration_Counter].xpos) + 1
                            x_range = x_distance//(bullet.Dr[2])
                            y_range = y_distance//(bullet.Dr[3])
                            if random.randint(0,x_range) == 0 and random.randint(0,y_range) == 0:
                                Barrier_Struck = True

                ## destroying the Barrier partlce
                if Barrier_Struck == True:
                    Barrier.pop(Barrier_Iteration_Counter)
                    Barrier_Struck = False
                else:
                    Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1
            break
        
def Update_Score(score):            
    if score.phrase[2] >= 10:
        score.phrase[1] = score.phrase[1] + 1
        score.phrase[2] = score.phrase[2] - 10
    if score.phrase[1] >= 10:
        score.phrase[0] = score.phrase[0] + 1
        score.phrase[1] = score.phrase[1] - 10
    if score.phrase[0] >= 10:
        score.phrase[0] = score.phrase[0] - 10
    
def Player_Explode(player):
    ## nonlocal declaration to variables and lists
    nonlocal alien_bullets, player_1_bullets, player_2_bullets
    nonlocal player_1, player_2, player_1_life, player_2_life
    nonlocal Flag_Gameover

    ## playing the sound
    Player_Explosion.Sound.play()                

    ## uploading the player_explosion images
    player_explosion = Player_Explosion(player.xpos,player.ypos,40,20)

    ## drawing the player_explosion
    for iteration in range(1,20):
        for animation in range(1,3):
            player_explosion.Draw(animation)
            Close_Or_Skip()
            pygame.display.update()
            clock.tick(15)
            
    ## emptying the player explosion from the screen by drawing a black rectangle
    player_explosion.Draw(3)
    
    ## drawing the player afterwards
    if player == player_1:
        if player_2 != None:
            player_2.Draw('blue')
            player_2.Flag_Movement_Direction = None
    elif player == player_2:
        if player_1 != None:
            player_1.Draw('green')
            player_1.Flag_Movement_Direction = None
    
    pygame.display.update()
    Pause(2)

    if player == player_1:
        if len(player_1_backup) != 0:

            ## resetting the player's attributes
            player_1.Flag_Movement_Direction = None
            player_1.Flag_Struck = False
            player_1.ypos = 400
            player_1.xpos = 50

            ## changing the player's lives
            player_1_backup.pop(-1)
            player_1_life.phrase[0] = player_1_life.phrase[0] - 1

        elif len(player_1_backup) == 0:

            ## removing the player from the game
            player_1 = None

    elif player == player_2:
        if len(player_2_backup) != 0:

            ## resetting the player's attributes
            player_2.Flag_Movement_Direction = None
            player_2.Flag_Struck = False
            player_2.ypos = 400
            player_2.xpos = 90
            
            ## changing the player's lives
            player_2_backup.pop(-1)
            player_2_life.phrase[0] = player_2_life.phrase[0] - 1

        elif len(player_2_backup) == 0:

            ## removing the player from the game
            player_2 = None

    ## checking if the game ends
    if player_1 == None and player_2 == None:
        Flag_Gameover = True

def Fill_Alien():

    ## nonlocal declaration to the lists and variables
    nonlocal aliens
    nonlocal Flag_Game_Level

    ## resetting all the alien attributes
    Alien.Timer = 20
    Alien.Animation = 0
    Alien.Flag_Collide_Side = None
    Alien.Flag_Down_Step = None
    Alien.Speed = 5

    ## resetting alien movement sounds and position moving down the screen afters each level
    Alien.Counter_Background_Sound = 1 

    ## layouts for various levels
    if Flag_Game_Level == [0,1]:
        alien_x_distance = 30
        alien_y_distance = 30
        alien_y_start_pos = 120
        alien_x_start_pos = 100
        alien_layout = [[1,1,1,1],
                        [1,1,1,1],
                        [1,1,1,1]]

    elif Flag_Game_Level == [0,2]:
        alien_x_distance = 30
        alien_y_distance = 30
        alien_y_start_pos = 120
        alien_x_start_pos = 100
        alien_layout = [[1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1]]
    
    elif Flag_Game_Level == [0,3]:
        alien_x_distance = 30
        alien_y_distance = 30
        alien_y_start_pos = 100
        alien_x_start_pos = 100
        alien_layout = [[0,0,1,1,0,0],
                        [0,1,1,1,1,0],
                        [1,1,1,1,1,1],
                        [1,1,1,1,1,1],
                        [0,1,1,1,1,0],
                        [0,0,1,1,0,0]]
        
    elif Flag_Game_Level == [0,4]:
        alien_x_distance = 20
        alien_y_distance = 20
        alien_y_start_pos = 120
        alien_x_start_pos = 100
        alien_layout = [[0,0,1,0,0,0,0,0,1,0,0],
                        [0,0,0,1,0,0,0,1,0,0,0],
                        [0,0,1,1,1,1,1,1,1,0,0],
                        [0,1,1,0,1,1,1,0,1,1,0],
                        [1,1,1,1,1,1,1,1,1,1,1],
                        [1,0,1,1,1,1,1,1,1,0,1],
                        [1,0,1,0,0,0,0,0,1,0,1],
                        [0,0,0,1,1,0,1,1,0,0,0]]

    elif Flag_Game_Level == [0,5]:
        alien_x_distance = 20
        alien_y_distance = 15
        alien_y_start_pos = 120
        alien_x_start_pos = 100
        alien_layout = [[1,1,0,0,0,0,0,0,1,1],
                        [1,1,0,0,0,0,0,0,1,1],
                        [1,1,0,0,0,0,0,0,1,1],
                        [1,1,0,0,2,0,0,0,1,1],
                        [0,1,1,0,0,0,0,1,1,0],
                        [0,1,1,0,0,0,0,1,1,0],
                        [0,1,1,0,0,0,0,1,1,0],
                        [0,0,1,1,0,0,1,1,0,0],
                        [0,0,1,1,0,0,1,1,0,0],                 
                        [0,0,0,1,1,1,1,0,0,0],  
                        [0,0,0,1,1,1,1,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0]]

    elif Flag_Game_Level == [0,6]:
        alien_x_distance = 30
        alien_y_distance = 30
        alien_y_start_pos = 100
        alien_x_start_pos = 120
        alien_layout = [[2,0,2,0,2,0,2],
                        [0,0,0,0,0,0,0],
                        [0,0,2,0,2,0,0],
                        [0,0,0,0,0,0,0],
                        [2,0,2,0,2,0,2]]
    
    elif Flag_Game_Level == [0,7]:
        alien_x_distance = 20
        alien_y_distance = 20
        alien_y_start_pos = 60
        alien_x_start_pos = 40
        alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,1,0,2,0,0,2,0,0,1,0,0,0],
                        [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                        [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
                        [0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
                        [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                        [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                        [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    elif Flag_Game_Level == [0,8]:
        alien_x_distance = 20
        alien_y_distance = 20
        alien_y_start_pos = 40
        alien_x_start_pos = 110
        alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,3,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1]]
    
    elif Flag_Game_Level == [0,9]:
        alien_x_distance = 20
        alien_y_distance = 20
        alien_y_start_pos = 100
        alien_x_start_pos = 60
        alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [3,0,0,0,0,0,3,0,0,0,0,0,3],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0]]
    
    elif Flag_Game_Level == [1,0]:
        alien_x_distance = 20
        alien_y_distance = 15
        alien_y_start_pos = 80
        alien_x_start_pos = 40
        alien_layout = [[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                        [0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0],
                        [0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0],
                        [0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                        [0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0],
                        [0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0],
                        [0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,0,0,0,0],
                        [0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,0,0,0,0],
                        [0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0],
                        [0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    elif Flag_Game_Level == [1,1]:
        alien_x_distance = 20
        alien_y_distance = 20
        alien_y_start_pos = 100
        alien_x_start_pos = 60
        alien_layout = [[0],
                        [4],
                        [0]]
        
    elif Flag_Game_Level == [1,2]:
        alien_x_distance = 30
        alien_y_distance = 30
        alien_y_start_pos = 80
        alien_x_start_pos = 60
        alien_layout = [[2,0,2,0,2,0,2,0,2],
                        [0,0,0,0,0,0,0,0,0],
                        [2,0,2,0,2,0,2,0,2],
                        [0,0,0,0,0,0,0,0,0],
                        [2,0,2,0,2,0,2,0,2],
                        [0,0,0,0,0,0,0,0,0],
                        [2,0,2,0,2,0,2,0,2]]
        
    elif Flag_Game_Level == [1,3]:
        alien_x_distance = 20
        alien_y_distance = 15
        alien_y_start_pos = 80
        alien_x_start_pos = 60
        alien_layout = [[1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
                        [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                        [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                        [0,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1],
                        [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                        [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                        [0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0],
                        [1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1],
                        [1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
                        [1,1,1,1,0,1,0,1,0,1,0,1,0,0,0,1],
                        [1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
                        [1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,1],
                        [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0]]
    
    elif Flag_Game_Level == [1,4]:
        alien_x_distance = 20
        alien_y_distance = 15
        alien_x_start_pos = 60
        alien_y_start_pos = 80
        alien_layout = [[1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1]]
    
    elif Flag_Game_Level == [1,5]:
        alien_x_distance = 20
        alien_y_distance = 15
        alien_x_start_pos = 60
        alien_y_start_pos = 80
        alien_layout = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    ## filling the aliens
    for row in range(len(alien_layout) - 1,-1,-1):
        for column in range(len(alien_layout[row]) - 1,-1,-1):
            if alien_layout[row][column] >= 1:
                ## checking if the level is 14 or if the level is 15 and adding only type 3 aliens
                if Flag_Game_Level == [1,4] or Flag_Game_Level == [1,5]:
                    aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,3,alien_layout[row][column]))

                ## checking if otherwise and adding the aliens to the list
                elif row > 3/5*len(alien_layout):
                    aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,2,alien_layout[row][column]))
                elif row > 1/5*len(alien_layout):
                    aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,1,alien_layout[row][column]))
                else:
                    aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,3,alien_layout[row][column]))

def Barrier_Refill():
    ## globalizing the Barrier lists
    nonlocal Barrier1,Barrier2,Barrier3,Barrier4,alien_invasion_line

    ## filling the Barrier lists
    for row in range(0,len(Barrier_layout)):
        for column in range(len(Barrier_layout[row])):
            if Barrier_layout[row][column] == 1:
                Barrier1.append(Barrier(column*2 + 48,row*2 + 330))
                Barrier2.append(Barrier(column*2 + 156,row*2 + 330))
                Barrier3.append(Barrier(column*2 + 264,row*2 + 330))
                Barrier4.append(Barrier(column*2 + 372,row*2 + 330))
    
    ## filling the alien invasion line
    for row in range(0,1):
        for column in range(0,480):
            alien_invasion_line.append(Barrier(column*2,row*2 + 435))

def Fill_Black():
    ## filling the screen quickly but not directly
    for xpos in range(0,480,120):
        pygame.draw.rect(screen,black,(xpos,0,120,480))
        Close_Or_Skip()
        pygame.display.update()
        clock.tick(20)

    ## making sure that the function doesn't happen again if the player has skipped
    nonlocal Flag_Skip
    if Flag_Skip == True:
        Flag_Skip  = 'stage_2'

def Screen_Draw(start_of_game = False): 

## limiting the process of drawing everything to be only at the start of the game 
    if start_of_game == True:
        screen.fill(black)

        ## drawing the score
        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()
        player_1_life.Draw()
        player_2_life.Draw()
        credit_message.Draw()

        ## drawing the floor
        for Barrier_particle in alien_invasion_line:
            Barrier_particle.Draw()

        ## drawing the Barrier
        for Barrier_particle in Barrier1:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier2:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier3:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier4:
            Barrier_particle.Draw()
        
        ## drawing the players 
        player_1.Draw('green')
        if player_2 != None:
            player_2.Draw('blue')
        for player in player_1_backup:
            player.Draw('green')
        for player in player_2_backup:
            player.Draw('blue')
    
## drawing the level message
    nonlocal Flag_Game_Level

    ## checking if the level is greater then 10 
    if Flag_Game_Level[0] > 0:

        ## preparing the level message 
        level_message = Words_And_Phrases(180,180,'LEVEL ' + str(Flag_Game_Level[0]) + str(Flag_Game_Level[1]))

        ## checking if the level is 14 and also writing a message
        if Flag_Game_Level == [1,4]:

            ## changing the level message's ypos and clearing space for the other message
            level_message.ypos = 120

            ## preparing level 14's other messages
            game_completion_message = [Words_And_Phrases(75,160,'CONGRATS.YOU BASICALLY'),
                                        Words_And_Phrases(105,195,'FINISHED THE GAME.'),
                                        Words_And_Phrases(105,230,'CAN YOU STILL BEAT'),
                                        Words_And_Phrases(60,265,'THIS LEVEL? IT GENERATES'), 
                                        Words_And_Phrases(128,300,'LOTS OF POINTS.')]

        ## checking if the level is 15 and also writing a message
        elif Flag_Game_Level == [1,5]:

            ## changing the level message's ypos and clearing space for the other message
            level_message.ypos = 120

            ## preparing level 15's other messages
            final_level_message = [Words_And_Phrases(38,160,'YOU REACHED THE FINAL LEVEL'),
                                    Words_And_Phrases(23,195,'OF THE ENTIRE GAME.IT IS LIKE'),
                                    Words_And_Phrases(38,230,'LEVEL 14 BUT WITH MANY MORE'),
                                    Words_And_Phrases(15,265,'ALIENS WHICH MAKES IT ALSO THE'),
                                    Words_And_Phrases(60,300,'HARDEST LEVEL.GOOD LUCK.')]

    ## checking if the level is less then 10
    else:

        ## preparing the level 
        level_message = Words_And_Phrases(187,180,'LEVEL ' + str(Flag_Game_Level[0]) + str(Flag_Game_Level[1]))

    ## drawing the level message
    level_message.Draw()

    ## checking if the level is 14 and drawing the other messages
    if Flag_Game_Level == [1,4]:
        for line in game_completion_message:
            line.Draw(6)
    
    ## checking if the level is 15 and drawing the message
    if Flag_Game_Level == [1,5]:
        for line in final_level_message:
            line.Draw(6)

    ## updating the screen and pausing it
    pygame.display.update()
    Pause(2)

    ## drawing a square to erase all messages
    pygame.draw.rect(screen,black,(0,75,480,255))
    
## drawing the aliens and closing the screen if the quit button is pressed
    for alien in aliens:
        alien.Draw('white')
        Close_Or_Skip()
        pygame.display.update()
        clock.tick(60)