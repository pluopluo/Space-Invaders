## importing files
import random
import pygame
from pygame.locals import *
from customcolors import *
from pygame import mixer

## setting up pygame, it's screen, caption, and clock
pygame.init()
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()                         

## setting up the game play
def MainGame():
    def Close_Skip_Check():
        nonlocal flag_skip    

        ## event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            ## checking if the player decides to skip
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if flag_skip == False:
                        flag_skip = True
        
        ## checking if the player has skipped
        if flag_skip == True:
            clock.tick(60)

            ## filling the screen quickly but not directly
            for xpos in range(0,480,60):
                pygame.draw.rect(screen,black,(xpos,0,60,480))

                ## quit check
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()

                pygame.display.update()
                clock.tick(40)
            
            ## setting flag skip with a new value showing the player already skipped
            flag_skip = 'stage_2'

    def Pause(time):
        num_of_time_units = int(time*60)

        ## iteration process
        for time_unit in range(0,num_of_time_units):
            
            ## checking if the player closes or skips
            Close_Skip_Check()
            if flag_skip == True or flag_skip == 'stage_2':
                break

            pygame.display.update()
            clock.tick(60)

    def Fill_Screen_Black():
        for xpos in range(0,480,60):
            pygame.draw.rect(screen,black,(xpos,0,60,480))

            Close_Skip_Check()
            if flag_skip == True or flag_skip == 'stage_2':
                break
            
            pygame.display.update()
            clock.tick(40)

    def Collide(object_1,object_2):
        if object_1.xpos + object_1.length > object_2.xpos and object_2.xpos + object_2.length > object_1.xpos:
            if object_1.ypos + object_1.height > object_2.ypos and object_2.ypos + object_2.height > object_1.ypos:
                return True

    def Bullet_Barrier_Collision(barrier,bullet):
        ## declaring nonlocals to the players and the bullet explosion list
        nonlocal player_1, player_2, alien_bullets, bullet_explosion_list
    
        ## checking what type of bullet it is and what iteration should be performed on the barrier
        if bullet in alien_bullets:
            barrier_iteration = [0,len(barrier),1]
        elif bullet in player_1.Bullet_List or bullet in player_2_bullets:
            barrier_iteration = [len(barrier) - 1,-1,-1]
         
        ## checking the barrier and if the divisor is supposed to be 2
        if barrier == alien_invasion_line:
            divisor = 2
        else:
            divisor = 1

        target_barrier = None
        ## checking the specific particle the bullet hits
        for barrier_index in range(barrier_iteration[0],barrier_iteration[1],barrier_iteration[2]):
            if Collide(bullet,barrier[barrier_index]) == True:

                # removing the barrier from the list
                if bullet in alien_bullets:
                    alien_bullets.remove(bullet)
                if bullet in player_1.Bullet_List:
                    player_1.Bullet_List.remove(bullet)
                if bullet in player_2_bullets:
                    player_2_bullets.remove(bullet)

                target_barrier = barrier[barrier_index]
                barrier_iteration_counter = 0
                flag_barrier_struck = False

                ## running through the barrier and checking which ones should disappear
                while True:

                    # breaking the while loop when the iteration process is done
                    if barrier_iteration_counter >= len(barrier):
                        break
                
                    ## checking if the xpos is correct from the ground shield
                    if barrier[barrier_iteration_counter].xpos%(divisor*2) == 0:

                        ## checking if the barrier particle is in close range of the area hit by the bullet
                        if target_barrier.xpos - bullet.Dr[0]*2 < barrier[barrier_iteration_counter].xpos < target_barrier.xpos + target_barrier.length + bullet.Dr[0]:
                            if target_barrier.ypos - bullet.Dr[1]*2 < barrier[barrier_iteration_counter].ypos < target_barrier.ypos + target_barrier.height + bullet.Dr[1]*2:
                                flag_barrier_struck = True
                            
                        ## checking if the barrier particle is in far range of the area struck by the bullet
                        if target_barrier.xpos - bullet.Dr[2]*2 < barrier[barrier_iteration_counter].xpos < target_barrier.xpos + target_barrier.height + bullet.Dr[2]*2:
                            if target_barrier.ypos - bullet.Dr[3]*2 < barrier[barrier_iteration_counter].ypos < target_barrier.ypos + target_barrier.height + bullet.Dr[3]*2:
                                # deciding how far it is and the chance of the barrier being destroyed
                                y_distance = abs(target_barrier.ypos - barrier[barrier_iteration_counter].ypos) + 1
                                x_distance = abs(target_barrier.xpos - barrier[barrier_iteration_counter].xpos) + 1
                                x_range = x_distance//(bullet.Dr[2])
                                y_range = y_distance//(bullet.Dr[3])
                                if random.randint(0,x_range) == 0 and random.randint(0,y_range) == 0:
                                    flag_barrier_struck = True

                    ## destroying the barrier partlce
                    if flag_barrier_struck == True:
                        barrier.pop(barrier_iteration_counter)
                        flag_barrier_struck = False

                    ## otherwise updating the barrier iteration counter
                    else:
                        barrier_iteration_counter = barrier_iteration_counter + 1
                break  ## breaking the for loop from no use 

    def Alien_Barrier_Collision(alien,barrier):
        barrier_iteration_counter = 0
        flag_barrier_struck = False

        ## iterating through the barriers
        while True:
            if barrier_iteration_counter == len(barrier):
                break

            ## checking if a barrier block hit the alien
            if alien.xpos + alien.length >= barrier[barrier_iteration_counter].xpos and alien.xpos <= barrier[barrier_iteration_counter].xpos + barrier[barrier_iteration_counter].length:
                if alien.ypos + alien.height >= barrier[barrier_iteration_counter].ypos:
                    flag_barrier_struck = True
            
            ## destroying the barrier block
            if flag_barrier_struck == True:
                barrier.pop(barrier_iteration_counter)
                flag_barrier_struck = False

            ## updating the iteration counter only if the barrier isn't destroyed
            else:
                barrier_iteration_counter = barrier_iteration_counter + 1

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
        nonlocal alien_bullets, player_1.Bullet_List, player_2_bullets
        nonlocal player_1, player_2, player_1_life, player_2.lives
        nonlocal flag_gameover
 
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
                player_1_life.phrase = player_1_life.phrase - 1

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
                player_2.lives.phrase = player_2.lives.phrase - 1

            elif len(player_2_backup) == 0:

                ## removing the player from the game
                player_2 = None

        ## checking if the game ends
        if player_1 == None and player_2 == None:
            flag_gameover = True

    def Fill_Alien():

        ## nonlocal declaration to the lists and variables
        nonlocal aliens
        nonlocal flag_game_level

        ## resetting all the alien attributes
        Alien.Timer = 20
        Alien.Animation = 0
        Alien.Flag_Collide_Side = None
        Alien.Flag_Down_Step = None
        Alien.Speed = 5

        ## resetting alien movement sounds and position moving down the screen afters each level
        Alien.Counter_Background_Sound = 1 

        ## layouts for various levels
        if flag_game_level == [0,1]:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[1,1,1,1],
                            [1,1,1,1],
                            [1,1,1,1]]
    
        elif flag_game_level == [0,2]:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1]]
        
        elif flag_game_level == [0,3]:
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
            
        elif flag_game_level == [0,4]:
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

        elif flag_game_level == [0,5]:
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

        elif flag_game_level == [0,6]:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 100
            alien_x_start_pos = 120
            alien_layout = [[2,0,2,0,2,0,2],
                            [0,0,0,0,0,0,0],
                            [0,0,2,0,2,0,0],
                            [0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2]]
        
        elif flag_game_level == [0,7]:
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

        elif flag_game_level == [0,8]:
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
        
        elif flag_game_level == [0,9]:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 100
            alien_x_start_pos = 60
            alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [3,0,0,0,0,0,3,0,0,0,0,0,3],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0]]
        
        elif flag_game_level == [1,0]:
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

        elif flag_game_level == [1,1]:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 100
            alien_x_start_pos = 60
            alien_layout = [[0],
                            [4],
                            [0]]
            
        elif flag_game_level == [1,2]:
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
            
        elif flag_game_level == [1,3]:
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
        
        elif flag_game_level == [1,4]:
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
        
        elif flag_game_level == [1,5]:
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
                    if flag_game_level == [1,4] or flag_game_level == [1,5]:
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
        nonlocal barrier1,barrier2,barrier3,barrier4,alien_invasion_line

        ## filling the Barrier lists
        for row in range(0,len(barrier_layout)):
            for column in range(len(barrier_layout[row])):
                if barrier_layout[row][column] == 1:
                    barrier1.append(Barrier(column*2 + 48,row*2 + 330))
                    barrier2.append(Barrier(column*2 + 156,row*2 + 330))
                    barrier3.append(Barrier(column*2 + 264,row*2 + 330))
                    barrier4.append(Barrier(column*2 + 372,row*2 + 330))
        
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
        nonlocal flag_skip
        if flag_skip == True:
            flag_skip = 'stage_2'

    def Screen_Draw(start_of_game = False): 
        ## defining a function to draw everything but the aliens
        def Draw_Elements_Except_Aliens():
            ## filling the screen black
            screen.fill(black)

            ## drawing the score
            score_message.Draw()
            player_1.Score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            player_1_life.Draw()
            player_2.lives.Draw()
            credit_message.Draw()

            ## drawing the floor
            for barrier_particle in alien_invasion_line:
                barrier_particle.Draw()

            ## drawing the Barrier
            for barrier_particle in barrier1:
                barrier_particle.Draw()
            for barrier_particle in barrier2:
                barrier_particle.Draw()
            for barrier_particle in barrier3:
                barrier_particle.Draw()
            for barrier_particle in barrier4:
                barrier_particle.Draw()
            
            ## drawing the players 
            player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in player_2_backup:
                player.Draw('blue')

    ## limiting the process of drawing everything but aliens to be only at the start of the game 
        if start_of_game == True:
            Draw_Elements_Except_Aliens()

    ## drawing the level message
        nonlocal flag_game_level

        ## preparing the level message
        level_message = [Game_Text('middle',180,'LEVEL ' + str(flag_game_level[0]) + str(flag_game_level[1]))]
        
        ## checking if the player started and writing a starter message
        if flag_game_level == [0,1]:

            ## preparing the first starter message
            starter_message_one = [Game_Text('middle',120,'WELCOME TO SPACE INVADERS 2.'),
                                   Game_Text('middle',145,'IT IS AN EXTENSION TO THE'),
                                   Game_Text('middle',170,'ORIGIANL SPACE INVADERS'),
                                   Game_Text('middle',195,'SO LOOK ON WEB HOW TO PLAY'),
                                   Game_Text('middle',220,'SPACE INVADERS IF YOU HAVE'),
                                   Game_Text('middle',245,'NOT ALREDY PLAYED IT.')]
        
            ## preparing the second starter message
            starter_message_two = [Game_Text('middle',120,'THE DIFFERENCES IN THIS'),
                                   Game_Text('middle',145,'GAME AND THE ORIGINAL GAME'),
                                   Game_Text('middle',170,'IS THAT THIS GAME HAS 15'),
                                   Game_Text('middle',195,'GAME LEVELS AND MANY'),
                                   Game_Text('middle',220,'UPGRADES BASED ON THE AMOUNT'),
                                   Game_Text('middle',245,'OF POINTS YOU HAVE.')]

            ## preparing the third starter message
            starter_message_three = [Game_Text('middle',120,'FIRST UPGRADE:YOU START'),
                                     Game_Text('middle',145,'WITH TWO LIVES AND GAIN'),
                                     Game_Text('middle',170,'AN ADDITIONAL LIFE FOR'),
                                     Game_Text('middle',195,'EVERY 500 POINTS YOU'),
                                     Game_Text('middle',220,'GET.MAX:3 LIVES.')]

            ## preparing the fourth starter message
            starter_message_four = [Game_Text('middle',120,'SECOND UPGRADE:YOU GAIN AN'),
                                    Game_Text('middle',145,'ADDITIONAL BULLET THAT'),
                                    Game_Text('middle',170,'YOU CAN SHOOT ONTO THE'),
                                    Game_Text('middle',195,'ALIENS AT A TIME FOR EVERY'),
                                    Game_Text('middle',220,'2000 POINTS YOU GET.THERE'),
                                    Game_Text('middle',245,'IS NO UPPER LIMIT.')]

            ## preparing the fifth starter message
            starter_message_five = [Game_Text('middle',120,'LASTLY:MORE AND MORE ALIENS'),
                                    Game_Text('middle',145,'WILL APPEAR AS THE LEVELS'),
                                    Game_Text('middle',170,'GETS HIGHER AND HIGHER.')]

        ## checking if the player reached level 14 and writing an additional message
        elif flag_game_level == [1,4]:

            ## preparing level 14's other messages
            game_completion_message = [Game_Text(75,145,'CONGRATS.YOU BASICALLY'),
                                       Game_Text(105,170,'FINISHED THE GAME.'),
                                       Game_Text(105,195,'CAN YOU STILL BEAT'),
                                       Game_Text(60,220,'LEVEL 14? IT GENERATES'), 
                                       Game_Text(128,245,'LOTS OF POINTS.')]

        ## checking if the player reached level 15 and also writing an additional message
        elif flag_game_level == [1,5]:

            ## preparing level 15's other messages
            final_level_message = [Game_Text(38,145,'YOU REACHED THE FINAL LEVEL'),
                                    Game_Text(23,170,'OF THE ENTIRE GAME.IT IS LIKE'),
                                    Game_Text(38,195,'LEVEL 14 BUT WITH MANY MORE'),
                                    Game_Text(15,220,'ALIENS WHICH MAKES IT ALSO THE'),
                                    Game_Text(60,245,'HARDEST LEVEL.GOOD LUCK.')]
            
        ## defining the function that draws, pauses and erases the screen
        def Draw_Game_Text(game_text):
            
            ## drawing the game text
            for line in game_text:
                line.Draw(6)
            
            ## pausing and erasing the screen by drawing a big rectangle
            Pause(2)
            pygame.draw.rect(screen,black,(0,75,480,255))

            ## updating the screen
            pygame.display.update()

            ## pausing a short time making more breathing space
            Pause(0.5)
            
        ## checking if the game started and drawing the message
        if flag_game_level == [0,1]:

            ## drawing the message
            Draw_Game_Text(starter_message_one)
            Draw_Game_Text(starter_message_two)
            Draw_Game_Text(starter_message_three)
            Draw_Game_Text(starter_message_four)
            Draw_Game_Text(starter_message_five)
        
        ## checking if the level is 14 and drawing a message
        if flag_game_level == [1,4]:

            ## drawing the message
            Draw_Game_Text(game_completion_message)
        
        ## checking if the level is 15 and drawing the message
        elif flag_game_level == [1,5]:

            ## drawing the message
            Draw_Game_Text(final_level_message)

    ## checking if everything should be drawn again

        ## globalizing flag skip
        nonlocal flag_skip

        ## checking process
        if flag_skip == 'stage_2':

            ## ending flag skip until the game restarts
            flag_skip = 'done'

            ## redrawing everything
            Draw_Elements_Except_Aliens()

        ## ending flag skip until the game restarts
        flag_skip = 'done'

        ## drawing the level message
        Draw_Game_Text(level_message)

    ## drawing the aliens and closing the screen if the quit button is pressed
        for alien in aliens:
            alien.Draw('white')
            Close_Or_Skip()
            pygame.display.update()
            clock.tick(60)

    ## main class
    class Game_Element:
        Basic_Sound_Url = 'Sounds\\'
        Basic_Url = 'Images\\'
        def __init__(self,xpos,ypos):
            self.xpos = xpos
            self.ypos = ypos

    class Game_Text(Game_Element):
        ## uploading all the character names
        Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                                'O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,
                                3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark',
                                'dash','space','yflip','period','colon']
        
        ## uploading all the character images, transforming it, and storing it in a dictionary with respective value
        Character_Dictionary = {}
        for character_name in Character_Name_List:

            ## loading the image, transforming it, then storing it
            img = pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg')
            img = pygame.transform.scale(img,(10,14))
            Character_Dictionary[character_name] = img
            
        def __init__(self,xpos,ypos,phrase):

            ## setting up the phrase of the class
            self.phrase = phrase

            ## setting up the ypos
            self.ypos = ypos

            ## checking if the xpos is used as the middle of the screen
            if xpos == 'middle':
                twice_middle = 480 - len(phrase)*15
                self.xpos = twice_middle/2
            
            ## checking if else:
            else:
                self.xpos = xpos

        def Draw(self,delay=0):

            ## setting up the counter spacing used for drawing 
            Counter_Spacing = 0

            ## iteration process
            for character in self.phrase:

                ## checking if the player decides to skip
                if Player_Selected == True:
                    if flag_skip == True or flag_skip == 'stage_2':
                        if flag_skip == True:
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
                elif character == ':':
                    character = 'colon'
                
                ## checking if the character is a string number and changing it to an integar
                string_number_list = ['0','1','2','3','4','5','6','7','8','9']
                if character in string_number_list:
                    character = int(character)
                
                ## drawing the letter and increasing the counter spacing
                screen.blit(Game_Text.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
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
            nonlocal flag_game_level

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
                    Alien_Barrier_Collision(self,barrier1)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Alien_Barrier_Collision(self,barrier2)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Alien_Barrier_Collision(self,barrier3)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Alien_Barrier_Collision(self,barrier4)

            # checking if the aliens hit the invasion line or invade
            if self.ypos + self.height >= 435:
                nonlocal flag_gameover
                flag_gameover = True

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
                    
                    ## checking where to add the alien explosion based on the alien type
                    if self.type == 3:
                        alien_explosion_list.append(Alien_Explosion(self.xpos,self.ypos))
                    
                    else:
                        alien_explosion_list.append(Alien_Explosion(self.xpos - 3,self.ypos))
                    
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

        ## bullet and score variables
        Bullet_List = []
        Score = 0

        ## upgrade counter variable
        Counter_Upgrade_Life = 0
        
        ## setting up the player's image
        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player green.jpeg')
        Green_Image = pygame.transform.scale(Img,(30,20))

        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player blue.jpeg')
        Blue_Image = pygame.transform.scale(Img,(30,20))

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 30
            self.height = 20

        def Move_Player(self):
            
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
            nonlocal player_1.Bullet_List, player_2_bullets
            nonlocal player_1.Score, player_2_score

            ## checking if the player_1.Bullet_List hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(barrier4,self)

            ## checking if the bullets hit the alien
            if self in player_1.Bullet_List or self in player_2_bullets:
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
                            if self in player_1.Bullet_List:
                                player_1.Bullet_List.remove(self)
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
                        if self in player_1.Bullet_List:
                            player_1.Bullet_List.remove(self)
                            player_1.Score.phrase[2] = player_1.Score.phrase[2] + increment
                        elif self in player_2_bullets:
                            player_2_bullets.remove(self)
                            player_1.Score.phrase[2] = player_1.Score.phrase[2] + increment
                        
                        ## checking if the player has 3 lives or less
                        if player_1_life.phrase < 3:

                            ## upgrading the player's counter life upgrade
                            player_1.Counter_Upgrade_Life = player_1.Counter_Upgrade_Life + increment*10

                            ## checking when to upgrade the player's life
                            if player_1.Counter_Upgrade_Life >= 500:

                                ## upgrading the player's life
                                player_1_life.phrase = player_1_life.phrase + 1

                        ## updating the high score
                        high_score.phrase[2] = high_score.phrase[2] + increment
                        break 

                    ## ending the iteration if the bullet is removed
                    if self not in player_1.Bullet_List and self not in player_2_bullets:
                        break

            ## checking if the bullet hits the mystery ship
            if self in player_1.Bullet_List:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 1 bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_1.Lucky_Shot == True:
                            if (player_1.Shoot_Iteration_Counter - 23)%15 == 0:
                                mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_1.Score.phrase[1] = player_1.Score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_1.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_1.Lucky_Shot == False:
                            mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_1.Score.phrase[1] = player_1.Score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2

                    ## checking if the player 1 bullet hits the mystery ship on the 23rd shot 
                        if player_1.Shoot_Iteration_Counter == 23:
                            player_1.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_1.Bullet_List.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()

            elif self in player_2_bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 2's bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_2.Lucky_Shot == True:
                            if (player_2.Shoot_Iteration_Counter - 23)%15 == 0:
                                mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_2_score.phrase[1] = player_1.Score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_2.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_2.Lucky_Shot == False:
                            mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
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
            Update_Score(player_1.Score)
            Update_Score(player_2_score)
            Update_Score(high_score)

            ## checking if the player bullet hits the top of the screen
            if self in player_1.Bullet_List or self in player_2_bullets:
                if self.ypos < 0:
                    if self in player_1.Bullet_List:
                        player_1.Bullet_List.remove(self)
                    elif self in player_2_bullets:
                        player_2_bullets.remove(self)
                    bullet_explosion_list.append(Bullet_Explosion(self.xpos - 6,self.ypos))

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
            nonlocal alien_bullets, bullet_explosion_list
            alien_bullets_length = len(alien_bullets)
            ## checking if the alien_bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(barrier4,self)

            ## checking if the alien_bullets hits the boundary line
            if self.ypos + self.height > 435 and len(alien_bullets) == alien_bullets_length:
                Bullet_Barrier_Collision(alien_invasion_line,self)
                if self in alien_bullets:
                    alien_bullets.remove(self)
                bullet_explosion_list.append(Bullet_Explosion(self.xpos - 3,self.ypos - 4,))

            ## checking if the alien_bullet hit the player bullet
            if len(alien_bullets) == alien_bullets_length:
                for bullet in player_1.Bullet_List:
                    if self.xpos + self.length > bullet.xpos and bullet.xpos + bullet.length > self.xpos and self.ypos + self.height > bullet.ypos and bullet.ypos + bullet.height > self.ypos:
                        player_1.Bullet_List.remove(bullet)
                        bullet_explosion_list.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
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
                        bullet_explosion_list.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
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
                nonlocal alien_explosion_list
                alien_explosion_list.remove(self)

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
                nonlocal mystery_ship_explosion_list
                mystery_ship_explosion_list.remove(self)

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
    
    ## The Game Loop
    while True:
## setting up the menu 1
        ## setting up the words and messages
        please_select_message = Game_Text('middle',140,'PLEASE SELECT')
        one_or_two_players_message = Game_Text('middle',180,'<1 OR 2 PLAYERS>')
        one_player_message = Game_Text(190,220,'1PLAYER')
        two_player_message = Game_Text(190,260,'2PLAYER')

        ## setting up the select asterisk
        asterisk = Game_Text(170,220,'*')

        ## setting up the important credit message
        credit_message = Game_Text(340,456,'CREDIT 00')

        ## setting up the flag variable to begin the game
        Player_Selected = False

        ## setting up the mode variable
        flag_game_mode = 'one_player'

        ## setting up the player's score and the high score
        score_message = Game_Text('middle',20,'SCORE<1> HI-SCORE SCORE<2>')
        player_1.Score = Game_Text(60,60,[1,0,0,0])
        player_2_score = Game_Text(320,60,[0,0,0,0])
        high_score = Game_Text(200,60,[0,0,0,0])

        while True:
            screen.fill(black)

            ## drawing the player's score
            score_message.Draw()
            player_1.Score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            credit_message.Draw()

            ## drawing the phrases
            please_select_message.Draw()
            one_or_two_players_message.Draw()
            one_player_message.Draw()
            two_player_message.Draw()
            asterisk.Draw()

            ## basic key functions
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        ## changing the asterik's position resetting the game mode
                        asterisk.ypos = 260
                        flag_game_mode = 'two_player'

                    elif event.key == K_UP:
                        ## changing the asterik's position resetting the game mode
                        asterisk.ypos = 220
                        flag_game_mode = 'one_player'

                    elif event.key == K_RETURN:
                        Player_Selected = True
                        
            pygame.display.update()
            clock.tick(60)
            if Player_Selected == True:
                break

## setting up the menu 2
        ## flag skip variable
        flag_skip = False

        ## emptying the screen
        screen.fill(black)
        
        # drawing the player's score and high score
        score_message.Draw()
        player_1.Score.Draw()
        player_2_score.Draw()
        high_score.Draw()
        credit_message.Draw()

        # setting up and drawing the words and messages
        play_message = Game_Text(210,150,'PLA')
        play_message.Draw(6)

        y_message = Game_Text(255,150,['yflip'])
        y_message.Draw(6)

        space_invaders_message = Game_Text('middle',190,'SPACE INVADERS')
        space_invaders_message.Draw(6)

        Pause(0.5)

        ## drawing the score_advance_table
        score_advance_table = Game_Text('middle',250,'*SCORE ADVANCE TABLE*')
        score_advance_table.Draw()

        ## drawing the alien display only if the player hasn't skipped
        if flag_skip == False:
            mystery_ship_display = Mystery_Ship(144,285)
            mystery_ship_display.Draw()
                
            alien_3_display = Alien(153,320,3,1)
            alien_3_display.Draw('white')

            alien_1_display = Alien(150,355,1,1)
            alien_1_display.Draw('white')

            alien_2_display = Alien(150,390,2,1)
            alien_2_display.Draw('white')

        ## drawing the alien values
        mystery_point_message = Game_Text(180,285,'=? MYSTERY')
        mystery_point_message.Draw(6)
        
        thirty_points_message = Game_Text(180,320,'=30 POINTS')
        thirty_points_message.Draw(6)

        twenty_points_message = Game_Text(180,355,'=20 POINTS')
        twenty_points_message.Draw(6)

        ten_points_message = Game_Text(180,390,'=10 POINTS')
        ten_points_message.Draw(6)

    ## setting up the short alien film

        # making the alien
        start_alien = Alien(605,149,3,1)
        start_alien.Speed = -5

        ## moving the alien towards the letter to take it
        while True:

            ## checking if the player decides to skip and the break the loop if that happens
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break

            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Draw()
            start_alien.Move_Alien(True)

            ## checking if the alien reaches the cordinate of 265 where it will take the letter
            if start_alien.xpos == 260:

                ## changing the alien speed
                start_alien.Speed = 5

                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## moving the alien away from the letter to take it away
        while True:

            ## checking if the player decides to skip and breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break
            
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()

            ## drawing the alien
            start_alien.Draw_Letter_Take()
            start_alien.Move_Alien(True)

            ## checking if the alien reaches the cordinate of 600 where it will flip the letter
            if start_alien.xpos == 600:

                ## changing the alien speed
                start_alien.Speed = -5

                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## moving the alien towards the letter to replace it
        while True:
            ## checking if the player decides to skip and breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break

            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()

            ## drawing the alien
            start_alien.Draw_Letter_Place()

            ## checking if the alien reaches the cordinate of 260 where it place the flipped letter
            if start_alien.xpos == 260:

                # flipping the letter
                y_message = Game_Text(255,150,'Y')

                ## changing the alien speed
                start_alien.Speed = 5

                pygame.display.update()
                clock.tick(30)
                break

            ## moving the alien
            start_alien.Move_Alien(True)

            pygame.display.update()
            clock.tick(30)
        
        ## moving the alien away from the letter
        while True:

            ## breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break

            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Move_Alien(True)
            start_alien.Draw()

            ## checking if the alien reaches the cordinate of 600 and ending the loop
            if start_alien.xpos == 600:
                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## deleting the start alien from no use
        del start_alien
        
    ## checking if the player hasn't skipped and setting up the menu 3 and menu 4
        if flag_skip == False:

        ## setting up the menu 3

            ## filling the screen black quickly but not directly
            Fill_Black()

            ## drawing the scores
            score_message.Draw()
            player_1.Score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            credit_message.Draw()

            ## drawing the buttons
            push_message = Game_Text('middle',180,'PUSH')
            push_message.Draw()

            ## drawing the message describing the one player buttons used
            if flag_game_mode == 'one_player':
                only_one_player_button_message = Game_Text('middle',230,'ONLY 1 PLAYER BUTTON')
                only_one_player_button_message.Draw()

            ## drawing the message describing the two player buttons used
            elif flag_game_mode == 'two_player':
                only_two_player_button_message = Game_Text('middle',230,'2 PLAYER BUTTON')
                only_two_player_button_message.Draw()
            
            ## updating the screen only without the flagskip variable
            pygame.display.update()
            Pause(2)

    
        ## setting up menu 4
            ## filling the screen black quickly but not directly
            Fill_Black()

            for time in range(1,30):
                screen.fill(black)

                ## checking if the player decides to skip and breaking from the for loop if it happened
                Close_Or_Skip()
                if flag_skip == True or flag_skip == 'stage_2':
                    if flag_skip == True:
                        Fill_Black()
                    break

                if flag_game_mode == 'one_player':
                    ## drawing the play player 1 message and blinking the player 1 score
                    play_one_player_message = Game_Text('middle',180,'PLAY PLAYER<1>')
                    play_one_player_message.Draw()
                    if time%2 == 0:
                        player_1.Score.Draw()

                if flag_game_mode == 'two_player':
                    ## drawing the play player 2 message and blinking the player 1 and the player 2 score 
                    play_two_player_message = Game_Text('middle',220,'PLAY PLAYER<2>')
                    play_two_player_message.Draw()
                    if time%2 == 0:
                        player_2_score.Draw()
                        player_1.Score.Draw()
                else:
                    player_2_score.Draw()

                ## drawing the rest of the score info and the credit message
                score_message.Draw()
                high_score.Draw()
                credit_message.Draw()

                pygame.display.update()
                clock.tick(15)

        ## restarting the flag skip for the screen draw
        flag_skip = False

        ## changing the credit's xpos if the player mode is 2 player
        if flag_game_mode == 'two_player':
            credit_message.xpos = 173

## setting up the elements
        ## setting up the Flag Game Level and Gameover FLag Variable
        flag_game_level = [1,4]
        flag_gameover = False

        ## setting up the player, their backup, and their live 
        player_1 = None
        player_2 = None
        player_1_backup = []
        player_2_backup = []
        player_1_life = Game_Text(10,456,[])
        player_2.lives = Game_Text(460,456,[])

        if flag_game_mode == 'one_player' or flag_game_mode == 'two_player':
            player_1 = Player(50,400)
            player_1_backup = [Player(30,450),Player(70,450)]
            player_1_life.phrase = 2
        if flag_game_mode == 'two_player':
            player_2 = Player(90,400)
            player_2_backup = [Player(420,450),Player(380,450)]
            player_2.lives.phrase = 2
            
        aliens = []
        Fill_Alien()

        ## alien attributes
        alien_explosion_list = []

        ## setting up the Mystery_Ship
        mystery_ship = Mystery_Ship(2500,40)
        mystery_ship_explosion_list = []
        
        ## setting up the Barrier layout
        barrier_layout = [[0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
                        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]]

        ## setting up the Barrier and alien invasion line
        barrier1 = []
        barrier2 = []
        barrier3 = []
        barrier4 = []
        alien_invasion_line = []
        Barrier_Refill()

        ## setting up the bullet lists
        player_1.Bullet_List = []
        player_2_bullets = []
        alien_bullets = []
        bullet_explosion_list = []
        
    # setting up the screen
        Fill_Black()
        Screen_Draw(True)

    ## starting the game
        while True:
            screen.fill(black)

        ## moving the player
            if player_1 != None:
                player_1.Move_Player()
            if player_2 != None:
                player_2.Move_Player()

        ## moving the mystery ship
            mystery_ship.Move_Mystery_Ship()
            mystery_ship.Play_Sound()

        ## moving aliens and changing animations only if there is at least one alien on the screen
            if len(alien_explosion_list) == 0:
                Alien.Timer = Alien.Timer - 1
                if  Alien.Timer <= 0:
                    Alien.Timer = 20

                    ## changing the aliens' animation
                    Alien.Change_Animation()

                    ## moving the aliens down whenever the aliens reach a side
                    if Alien.Flag_Collide_Side != None:
                        for alien in aliens:
                            alien.Move_Down()
                            alien.Shoot()
                            alien.Check()

                        ## checking the requirements to generate new aliens
                        if flag_game_level == [1,4] or flag_game_level == [1,5]:

                            ## generating the upper range based on the level
                            if flag_game_level == [1,4]:
                                upper_range = len(aliens) - 13
                            elif flag_game_level == [1,5]:
                                upper_range = len(aliens) - 17

                            ## iterating through the aliens list
                            for iteration in range(len(aliens) - 1,upper_range,-1):

                                ## adding the new alien to the game
                                aliens[iteration].Copy_Alien()

                    ## moving the aliens regularly
                    elif Alien.Flag_Collide_Side == None:
                        for alien in aliens:
                            alien.Move_Alien()
                            alien.Shoot()
                            alien.Check()
                    
                ## playing the background music of the alien movement
                    mixer.music.load(Game_Element.Basic_Sound_Url+'background sound '+str(Alien.Counter_Background_Sound)+'.wav')
                    mixer.music.play()
                    Alien.Counter_Background_Sound = Alien.Counter_Background_Sound + 1
                    if Alien.Counter_Background_Sound == 5:
                        Alien.Counter_Background_Sound = 1

        ## moving the alien bullets
            alien_bullet_iteration_counter = 0
            while True:
                if alien_bullet_iteration_counter >= len(alien_bullets):
                    break
                alien_bullets_length = len(alien_bullets)
                alien_bullets[alien_bullet_iteration_counter].Move_Alien_Bullet()
                alien_bullets[alien_bullet_iteration_counter].Check()
                if len(alien_bullets) == alien_bullets_length:
                    alien_bullet_iteration_counter = alien_bullet_iteration_counter + 1

        ## moving the player bullets
            for bullet in player_1.Bullet_List:
                bullet.Move_Bullet()
                bullet.Check()
            for bullet in player_2_bullets:
                bullet.Move_Bullet()
                bullet.Check()

        ## updating the alien dead timer
            Alien_Explosion_Iteration_Counter = 0
            while True:
                if Alien_Explosion_Iteration_Counter == len(alien_explosion_list):
                    break
                Alien_Explosion_Length = len(alien_explosion_list)
                alien_explosion_list[Alien_Explosion_Iteration_Counter].Update_Timer()
                if Alien_Explosion_Length == len(alien_explosion_list):
                    Alien_Explosion_Iteration_Counter = Alien_Explosion_Iteration_Counter + 1
            
            Mystery_Ship_Explosion_Iteration_Counter = 0
            while True:
                if Mystery_Ship_Explosion_Iteration_Counter == len(mystery_ship_explosion_list):
                    break
                Mystery_Ship_Explosion_Length = len(mystery_ship_explosion_list)
                mystery_ship_explosion_list[Mystery_Ship_Explosion_Iteration_Counter].Update_Timer()
                if Mystery_Ship_Explosion_Length == len(mystery_ship_explosion_list):
                    Mystery_Ship_Explosion_Iteration_Counter = Mystery_Ship_Explosion_Iteration_Counter + 1
 
            ## The Key Loop
            for event in pygame.event.get():
                ## quit 
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'right'
                        else:
                            player_2.Flag_Movement_Direction = 'right'

                    elif event.key == K_LEFT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'left'
                        else:
                            player_2.Flag_Movement_Direction = 'left'

                    elif event.key == K_a:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'left'
                        else:
                            player_1.Flag_Movement_Direction = 'left'

                    elif event.key == K_d:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'right'
                        else:
                            player_1.Flag_Movement_Direction = 'right'

                ## shooting bullets using space
                    if event.key == K_SPACE:
                        if player_1 != None:

                            if len(player_1.Bullet_List) <= max_player_1.Bullet_List:
                                player_1.Shoot_Iteration_Counter = player_1.Shoot_Iteration_Counter + 1
                                player_1.Bullet_List.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()
                            
                        else:

                            if len(player_2_bullets) <= max_player_1.Bullet_List:
                                player_2.Shoot_Iteration_Counter = player_2.Shoot_Iteration_Counter + 1
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                ## shooting bullets using x
                    if event.key == K_x: 
                        if player_2 != None:
                            if len(player_2_bullets) <= max_player_2_bullets:
                                player_2.Shoot_Iteration_Counter = player_2.Shoot_Iteration_Counter + 1
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                        else:
                            if len(player_1.Bullet_List) <= max_player_2_bullets:
                                player_1.Shoot_Iteration_Counter = player_1.Shoot_Iteration_Counter + 1
                                player_1.Bullet_List.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                ## checking if the keys are lifted
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                    elif event.key == K_LEFT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                    if event.key == K_a:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                    elif event.key == K_d:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None

    ## drawing things 
        ## drawing the alien invasion line
            for barrier_particle in alien_invasion_line:
                barrier_particle.Draw()

        ## drawing the score
            score_message.Draw()
            player_1.Score.Draw()
            player_2_score.Draw()
            high_score.Draw()            
            player_1_life.Draw()
            player_2.lives.Draw()
            credit_message.Draw()

        ## drawing the player
            if player_1 != None:
                player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in player_2_backup:
                player.Draw('blue')
            
        ## drawing the Barriers
            for barrier_particle in barrier1:
                barrier_particle.Draw()
            for barrier_particle in barrier2:
                barrier_particle.Draw()
            for barrier_particle in barrier3:
                barrier_particle.Draw()
            for barrier_particle in barrier4:
                barrier_particle.Draw()
                
        ## drawing the Mystery_Ship
            mystery_ship.Draw()

        ## drawing the aliens
            for alien in aliens:
                if alien.ypos >= 315:
                    alien.Draw('green')
                else:
                    alien.Draw('white')

        ## drawing the Alien_Explosion and Mystery Ship Explosion
            for explosion in alien_explosion_list:
                explosion.Draw()
            for explosion in mystery_ship_explosion_list:
                explosion.Draw()
                
        ## drawing the player bullet with the specific color
            for bullet in player_1.Bullet_List:
                if flag_game_mode == 'two_player':
                    bullet.Draw('green')
                else:
                    bullet.Draw('white')
            for bullet in player_2_bullets:
                bullet.Draw('blue')
            
        ## drawing the alien bullets;
            for bullet in alien_bullets:
                bullet.Draw()
                
        ##drawing the explosion caused by the player and alien bullets
            bullet_explosion_Iteration_Counter = 0
            while True:
                if bullet_explosion_Iteration_Counter == len(bullet_explosion_list):
                    break
                bullet_explosion_list[bullet_explosion_Iteration_Counter].Draw()
                bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer = bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer - 1
                if bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer == 0:
                    bullet_explosion_list.pop(bullet_explosion_Iteration_Counter)
                else:
                    bullet_explosion_Iteration_Counter = bullet_explosion_Iteration_Counter + 1

        ## updating the windo
            pygame.display.update()
            clock.tick(60)

            ## checking if all the aliens are shot
            if len(aliens) == 0 and len(alien_explosion_list) == 0:
                ## emptying all the bullet lists
                alien_bullets = []
                player_1.Bullet_List = []
                player_2_bullets = []

                ## making the players stop
                if player_1 != None:
                    player_1.Flag_Movement_Direction = None
                elif player_2 != None:
                    player_2.Flag_Movement_Direction = None

                ## increasing the level of the game
                flag_game_level[1] = flag_game_level[1] + 1

                ## inreasing the level of the game by the tens place
                if flag_game_level[1] > 9:
                    flag_game_level[0] = flag_game_level[0] + 1
                    flag_game_level[1] = flag_game_level[1] - 10

                ## Refilling Aliens and Barriers
                Fill_Alien()
                Barrier_Refill()

                ## calling screen draw function 
                Screen_Draw()

        ## checking if the players are hit
            if player_1 != None:
                if player_1.Flag_Struck == True:
                    Player_Explode(player_1)

            if player_2 != None:
                if player_2.Flag_Struck == True:
                    Player_Explode(player_2)

        ## ending the game
            if flag_gameover == True:
                ## drawing the Game Over Sign
                game_over_message = Game_Text('middle',120,'GAMEOVER')
                game_over_message.Draw()
                pygame.display.update()
                Pause(2)
                break
MainGame()