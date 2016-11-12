#1-Import library
import pygame
import random
import sys
from pygame.locals import *

#2-Initialization
pygame.init()
pygame.mixer.init()
#----------------------------
#<Game Variable for Changing>
#set screen boundary
BOUND_W = 500  #boundary of width
BOUND_H = 600  #boundary of height
width, height = BOUND_W, BOUND_H
screen = pygame.display.set_mode((width, height))
#velocity & gravity
START_V = 0.1
START_G = 0.0025
velocity = START_V
gravity = START_G
#set bird & pipe's position
BIRD_X = 200  #bird's start x position
BIRD_Y = 200  #bird's start y position
bird_y = BIRD_Y
PIPE_X = 600  #pipe's x position
PIPE_Y_L = 580  #low pipe's y position
PIPE_Y_H = 20  #high pipe's y position
#gap width
GAP_MIN = 300
GAP_MAX = 500
#</Game Variable for Changing>
#-----------------------------
#pipes list, 3 element, [pipe png,x,y]
pipes_l = []
pipes_h = []
#flag for new pipe
newpipe_l = False
newpipe_h = False
#score
score = 0 #existing pipe's score count
previousscore = 0 #past pipe's score count
#key
key = False #True if SPACE is pressed
key_firstPressed = False #True once for pressing SPACE, will be False if keep pressing
key_previous = False #record the previous key
#set font
font = pygame.font.SysFont("Arial", 24)
scoretext = font.render(str(score+previousscore), True, (0,0,0))
textRect = scoretext.get_rect()
textRect.topleft=[20,20]

#3-Load images
bird = pygame.image.load("resources/image/bird.png")
pipe = pygame.image.load("resources/image/pipe.png")
pipe_2 = pygame.image.load("resources/image/pipe_2.png")
pipe_3 = pygame.image.load("resources/image/pipe_3.png")
pipe_4 = pygame.image.load("resources/image/pipe_4.png")
pipe_5 = pygame.image.load("resources/image/pipe_5.png")
pipe_6 = pygame.image.load("resources/image/pipe_6.png")
gameover = pygame.image.load("resources/image/gameover.png")
flapSound = pygame.mixer.Sound("resources/audio/jump.wav")
hit = pygame.mixer.Sound("resources/audio/explode.wav")
flapSound.set_volume(0.1)
hit.set_volume(0.1)
#4-Select pipe png
def selectpipe(a):
    if a == 1:
        return pipe
    elif a == 2:
        return pipe_2
    elif a == 3:
        return pipe_3
    elif a == 4:
        return pipe_4
    elif a == 5:
        return pipe_5
    elif a == 6:
        return pipe_6
    else:
        return pipe

#5-Key detection
def keydetection():
    global key
    global key_firstPressed
    global key_previous

    #update events
    for event in pygame.event.get():
        #detect mouse click to close the window
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            #detect key: SPACE
            if event.key == pygame.K_SPACE:
                #detect if it's the first time pressed the key
                if key_previous == True:
                    key_firstPressed = False
                else:
                    key_firstPressed = True
                #anyway, set key value true
                key = True
            #detect ESC to exit the game
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_SPACE:
                key = False
    #update previous key value
    #it's necessary to keep it out of the for loop or there'll be functional err 
    key_previous = key

#6-Initialize
def initialization(pipes_l,pipes_h):
    global GAP_MIN
    global GAP_MAX
    global PIPE_X
    global PIPE_Y_L
    global PIPE_Y_H
    global BIRD_Y
    global START_V

    global previousscore
    global bird_y
    global velocity

    #remove all from list pipes
    del pipes_l[:]
    del pipes_h[:]
    #set pipes
    i=1
    for _ in range(4):
        pipe_l = random.randint(1,6)
        pipe_h = 7-pipe_l
        gap = random.randint(GAP_MIN,GAP_MAX)
        pipes_l.append([selectpipe(pipe_l),(PIPE_X+GAP_MIN*i),PIPE_Y_L-50*pipe_l])
        pipes_h.append([selectpipe(pipe_h),(PIPE_X+GAP_MIN*i),PIPE_Y_H])
        i+=1
    #reset score
    previousscore = 0
    #reset bird
    bird_y = BIRD_Y
    velocity = START_V

#7-Main Function
running = 1
exitcode = 0
initialization(pipes_l,pipes_h)

while 1:
    while running:

        #<draw>-------------------------------------------------------------------------
        
        #clear screen and fill the background color
        screen.fill((0,255,255))
        
        #draw bird
        screen.blit(bird,(BIRD_X,bird_y))
        
        #draw pipes
        #the lower pipes
        for onepipe in pipes_l:
            index = 0
            #draw one pipe
            screen.blit(onepipe[0],(onepipe[1],onepipe[2]))
            #moving the pipe
            onepipe[1]-=0.5
            #kill the old pipe
            if onepipe[1] < 100:
                pipes_l.pop(index)
                #set appending new pipe flag
                newpipe_l = True
            index+=1
            #record the old pipe's x position
            endpipe = onepipe[1]
        #append a new pipe to the end of pipes
        if newpipe_l:
            #set random pipe height, in this case, how many pipes per pipe
            pipe_l = random.randint(1,6)
            pipe_h = 7-pipe_l
            #set random pipe gap
            gap = random.randint(GAP_MIN,GAP_MAX)
            #append a new pipe
            pipes_l.append([selectpipe(pipe_l),endpipe+gap,PIPE_Y_L-50*pipe_l])
            newpipe_l = False
            #count the score for the old pipe
            previousscore +=1
        #the higher pipes, basically the same with the lower pipes
        #two difference, don't need to count the previous score again; gap & pipe_h have been calculated
        for onepipe in pipes_h:
            index = 0
            screen.blit(onepipe[0],(onepipe[1],onepipe[2]))
            onepipe[1]-=0.5
            if onepipe[1] < 100:
                pipes_h.pop(index)
                newpipe_h = True
            index+=1
            endpipe = onepipe[1]
        if newpipe_h:
            pipes_h.append([selectpipe(pipe_h),endpipe+gap,PIPE_Y_H])
            newpipe_h = False
        
        #draw score
        scoretext = font.render(str(score+previousscore), True, (0,0,0))    
        screen.blit(scoretext, textRect)
        #every loop reset score because score will +1 for every past existing pipes every loop
        score = 0

        #update the screen
        pygame.display.flip()
        
        #</draw>-------------------------------------------------------------------------
        
        #add gravity
        velocity += gravity
        bird_y+=velocity
        #set boundary
        if bird_y <= -60: #60 is just a little bigger than the size of birds
            #change bird's position
            bird_y-=velocity
        elif bird_y >= BOUND_H: #out of boundary
            #bird die, stop the game, restart
            bird_y = -60
            velocity = START_V
            gravity = START_G
        #Flap bird
        #when the bird is upping, do not allow another flap, only when bird's going down, listen to keyboard
        keydetection()
        #flap
        if key_firstPressed == True:
            flapSound.play()
            velocity = -START_V*5
            #set the max velocity change a flap can do
            # if velocity < -START_V*5:
            #     velocity = -START_V*5
            key_firstPressed = False

        #Collision
        #define bird's rectangle
        birdrect = pygame.Rect(bird.get_rect())
        birdrect.left = BIRD_X
        birdrect.top = bird_y
        #define pipes' rectangle
        for p in pipes_l:
            prect= pygame.Rect(p[0].get_rect())
            prect.left = p[1]
            prect.top = p[2]
            if prect.colliderect(birdrect):
                #stop the game
                hit.play()
                pygame.time.wait(1000)
                running=0
                exitcode=1
            if (prect.left+50) < BIRD_X:
                score += 1
        for p in pipes_h:
            prect= pygame.Rect(p[0].get_rect())
            prect.left = p[1]
            prect.top = p[2]
            if prect.colliderect(birdrect):
                hit.play()
                pygame.time.wait(1000)
                running=0
                exitcode=1
    #one time exitcode strategy
    if exitcode:
        exitfont = pygame.font.SysFont("Arial", 50)
        restartfont = pygame.font.SysFont("Arial", 30)
        exitText = exitfont.render(str(score+previousscore), True, (255,0,0))
        restartText = restartfont.render("Press SPACE to restart", True, (0,0,0))
        exitTextRect = exitText.get_rect()
        restartTextRect = restartText.get_rect()
        exitTextRect.centerx = screen.get_rect().centerx
        exitTextRect.centery = screen.get_rect().centery
        restartTextRect.centerx = exitTextRect.centerx
        restartTextRect.centery = exitTextRect.centery+100
        screen.blit(gameover, (0,0))
        screen.blit(exitText, exitTextRect)
        screen.blit(restartText,restartTextRect)
    #looping exit strategy
    while exitcode:    
        pygame.display.flip()
        keydetection()
        if key == True :
            running = 1
            exitcode = 0
            initialization(pipes_l,pipes_h)