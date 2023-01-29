from os import environ,system
import math
import random
try:
    from screeninfo import get_monitors
except ImportError:
    system('pip install screeninfo')
    from screeninfo import get_monitors
width,height=0,0
monId=-1
for monitor in get_monitors():
    monId+=1
    if monitor.is_primary:
        width=monitor.width/2
        height=monitor.height/2
        break
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
    import pygame
except ImportError:
    system('pip install pygame')
    import pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height),display=monId)
running = True

movingUp = False
movingDown = False

FPS=240
playerpos = 0.5
playersize = 0.15
playerSpeed = 1

player2pos = 0.5

ballX = width/2
ballY = height/2
ballSize = width/100
ballVelX = width/2
ballVelY = 0
pauseTimer = 1

def drawTrackPoint(x,y):
    pygame.draw.rect(screen,(0,255,0),(x-7,y-7,14,14))

def ballPredict():
    paddlePos=width-(width/40)
    tempballX=ballX
    tempballY=ballY
    tempballVelX=ballVelX
    tempballVelY=ballVelY
    dist=(paddlePos-tempballX)/tempballVelX
    calcY=tempballY+(tempballVelY*dist)
    while True:
        if calcY > ballSize/2 and calcY < height-ballSize/2:
            drawTrackPoint(paddlePos,calcY)
            break
        else:
            if calcY < ballSize/2:
                pushback=((calcY)/tempballVelY)
            else:
                pushback=((calcY-(height-ballSize/2))/tempballVelY)
            dist=dist-pushback
            px=tempballX+(tempballVelX*dist)
            py=tempballY+(tempballVelY*dist)
            tempballX=px
            tempballY=py
            tempballVelY*=-1
            dist=(paddlePos-tempballX)/tempballVelX
            calcY=tempballY+(tempballVelY*dist)
            drawTrackPoint(px,py)
    return calcY/height

while running:
    screen.fill((24,24,24))
    #input
    for event in pygame.event.get():
        if event.type == 256:
            running = False
        elif event.type == 768:
            if event.key == 119 or event.key == 1073741906:
                movingUp = True
            elif event.key == 115 or event.key == 1073741905:
                movingDown = True
        elif event.type == 769:
            if event.key == 119 or event.key == 1073741906:
                movingUp = False
            elif event.key == 115 or event.key == 1073741905:
                movingDown = False
    
    #logic
    tick=clock.tick(FPS)/1000
    if pauseTimer <= 0:
        if movingUp and movingDown:
            pass
        elif movingUp:
            playerpos-=playerSpeed*tick
        elif movingDown:
            playerpos+=playerSpeed*tick

        #AI
        movingUp2 = False
        movingDown2 = False
        if ballVelX < 0:
            if 0.5 > player2pos:
                movingDown2 = True
            elif 0.5 < player2pos:
                movingUp2 = True
        else:
            target=ballPredict()
            if target > player2pos:
                movingDown2 = True
            elif target < player2pos:
                movingUp2 = True
        
        #end AI

        if movingUp2 and movingDown2:
            pass
        elif movingUp2:
            player2pos-=playerSpeed*tick
        elif movingDown2:
            player2pos+=playerSpeed*tick
        playerpos=max(playersize/2, min(playerpos, 1-(playersize/2))) 
        player2pos=max(playersize/2, min(player2pos, 1-(playersize/2)))
        
        ballX+=ballVelX*tick
        ballY+=ballVelY*tick
        if ballX >= (width-(width/40))-ballSize/2 and ballVelX > 0:
            if ballY <= height*player2pos+(height*(playersize/2)) and ballY >= (height*player2pos)-(height*(playersize/2)):
                ballVelX*=-1.05
                ballVelY=random.randrange(math.floor(ballVelX),math.floor(-ballVelX))
                ballX=(width-width/40)-((width-width/40)-ballX)
            else:
                if ballX > width-ballSize/2:
                    pauseTimer = 1
        elif ballX <= width/40+ballSize/2 and ballVelX < 0:
            if ballY <= height*playerpos+(height*(playersize/2)) and ballY >= (height*playerpos)-(height*(playersize/2)):
                ballVelX*=-1.05
                ballVelY=random.randrange(math.floor(-ballVelX),math.floor(ballVelX))
                ballX=(width/40)+((width/40)-ballX)
            else:
                if ballX < 0+ballSize/2:
                    pauseTimer = 1

        if ballY <= ballSize/2:
            ballVelY*=-1
            ballY = ballSize/2+(ballSize/2-ballY)
        elif ballY >= height-ballSize/2:
            ballVelY*=-1
            ballY = (height-ballSize/2)+((height-ballSize/2)-ballY)
    else:
        ballX = width/2
        ballY = height/2
        ballSize = width/100
        ballVelX = width/2
        ballVelY = 0
        player2pos = 0.5
        playerpos = 0.5
        pauseTimer-=tick
    
    #rendering
    pygame.draw.rect(screen,(255,255,255),(width/80,(height*playerpos)-((height*playersize)/2),width/80,height*playersize))
    pygame.draw.rect(screen,(255,255,255),(width-width/40,(height*player2pos)-((height*playersize)/2),width/80,height*playersize))
    pygame.draw.rect(screen,(255,255,255),(ballX-ballSize/2,ballY-ballSize/2,ballSize,ballSize))
    pygame.display.flip()
