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
        width=monitor.width/1.1
        height=monitor.height/1.1
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

FPS=240
playerpos = 0.5
playersize = 0.15
playerSpeed = 1.5

player2pos = 0.5

ballX = width/2
ballY = height/2
ballSize = width/100
ballVelX = width/2
velIncrease = width/40
ballVelY = 0
pauseTimer = 1

queuedRects=[]
last=""
def playsound(snd,vol):
    global last
    if snd==last:pygame.mixer.music.set_volume(vol);pygame.mixer.music.play()
    else:pygame.mixer.music.load("snd/"+snd);pygame.mixer.music.set_volume(vol);pygame.mixer.music.play()
    last=snd

def drawTrackPoint(x,y,lx,ly):
    pygame.draw.line(screen,(127,64,0),(lx,ly),(x,y),width=1)
    queuedRects.append((x-7,y-7,14,14))

def ballPredict(paddlePos):
    tempballX=ballX
    tempballY=ballY
    tempballVelX=ballVelX
    tempballVelY=ballVelY
    dist=(paddlePos-tempballX)/tempballVelX
    calcY=tempballY+(tempballVelY*dist)
    totalCalculations=0
    while True:
        totalCalculations+=1
        if calcY > ballSize/2 and calcY < height-ballSize/2:
            drawTrackPoint(paddlePos,calcY,tempballX,tempballY)
            break
        else:
            if calcY < ballSize/2:
                pushback=((calcY)/tempballVelY)
            else:
                pushback=((calcY-(height-ballSize/2))/tempballVelY)
            dist=dist-pushback
            px=tempballX+(tempballVelX*dist)
            py=tempballY+(tempballVelY*dist)
            drawTrackPoint(px,py,tempballX,tempballY)
            tempballX=px
            tempballY=py
            tempballVelY*=-1
            dist=(paddlePos-tempballX)/tempballVelX
            calcY=tempballY+(tempballVelY*dist)
        if totalCalculations == 3:
            break
    return calcY/height
playsound("win.wav",1)
while running:
    screen.fill((24,24,24))
    for event in pygame.event.get():
        if event.type == 256:
            running = False
    #logic
    tick=clock.tick(FPS)/1000
    if pauseTimer <= 0:
        movingUp = False
        movingDown = False
        if ballVelX > 0:
            if 0.5 > playerpos:
                movingDown = True
            elif 0.5 < playerpos:
                movingUp = True
        else:
            target=ballPredict(width/40)
            if target > playerpos:
                movingDown = True
            elif target < playerpos:
                movingUp = True
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
            target=ballPredict(width-(width/40))
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
                ballVelX+=velIncrease
                ballVelX*=-1
                playsound("paddle.wav",1)
                ballVelY=random.randrange(math.floor(ballVelX/1.5),math.floor(-ballVelX/1.5))
                ballX=(width-width/40)-((width-width/40)-ballX)
            else:
                if ballX > width-ballSize/2:
                    pauseTimer = 1
                    playsound("win.wav",1)
        elif ballX <= width/40+ballSize/2 and ballVelX < 0:
            if ballY <= height*playerpos+(height*(playersize/2)) and ballY >= (height*playerpos)-(height*(playersize/2)):
                ballVelX*=-1
                ballVelX+=velIncrease
                playsound("paddle.wav",1)
                ballVelY=random.randrange(math.floor(-ballVelX/1.5),math.floor(ballVelX/1.5))
                ballX=(width/40)+((width/40)-ballX)
            else:
                if ballX < 0+ballSize/2:
                    pauseTimer = 1
                    playsound("win.wav",1)

        if ballY <= ballSize/2:
            ballVelY*=-1
            ballY = ballSize/2+(ballSize/2-ballY)
            playsound("bounce.wav",1)
        elif ballY >= height-ballSize/2:
            ballVelY*=-1
            ballY = (height-ballSize/2)+((height-ballSize/2)-ballY)
            playsound("bounce.wav",1)
    else:
        ballX = width/2
        ballY = height/2
        ballSize = width/100
        ballVelX = width/2
        ballVelY = 0
        player2pos = 0.5
        playerpos = 0.5
        pauseTimer-=tick
        if pauseTimer <= 0:
            playsound("start.wav",1)
    
    #rendering
    for x in queuedRects:
        pygame.draw.rect(screen,(0,127,0),x)
    queuedRects=[]
    pygame.draw.rect(screen,(255,255,255),(width/80,(height*playerpos)-((height*playersize)/2),width/80,height*playersize))
    pygame.draw.rect(screen,(255,255,255),(width-width/40,(height*player2pos)-((height*playersize)/2),width/80,height*playersize))
    pygame.draw.rect(screen,(255,255,255),(ballX-ballSize/2,ballY-ballSize/2,ballSize,ballSize))
    pygame.display.flip()
