
#Main File
import draw
import decimal
import random
import copy
from signals import *
from draw import *
from allbeams import *
from obstacle import *
from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

#from CMU 112 course page, homeworks etc. (almostEqual, roundHalfUp, rgbString)
def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
  # note: use math.isclose() outside 15-112 with Python version 3.5 or later
  return (abs(d2 - d1) < epsilon)


def roundHalfUp(d): #helper-fn
  # Round to nearest with ties going away from zero.
  rounding = decimal.ROUND_HALF_UP
  return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
 
def rgbString(red, green, blue):
   return f'#{red:02x}{green:02x}{blue:02x}'

def calcDistance(x0, y0, x1, y1):
   xdist = x1 - x0
   ydist = y1 - y0
   return (xdist**2 + ydist**2)**0.5

#Features:
# multiple levels that increase complexity
# ability to get a certain number of points and boost
# different modes (avoid crashing into other signals) 
  
#########################################################################
# APP STARTED
#########################################################################
 
class randSignal(object):
    def __init__(self, cx, cy):
        self.radius = 5
        self.cx = cx
        self.cy = cy
        self.speedx = 5
        self.speedy = 5
        self.shiftFactor = -1
        self.active = True

class signal(object):
    def __init__(self, cx, cy): #add app.margin for y if needed?
        self.cx = cx
        self.cy = cy
        colors = ['red', 'orange', 'blue', 'green']
        self.fill = 'black'
        self.r = 5

class obstacle(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.fill = 'red'
        self.r = 5


def appStarted(app):
  app.gravity = -3.2
  app.acceleration = 3.2
  app.velocity = -18
  app.level = 2
  app.width = 400
  app.height = 400
  app.margin = min(app.width, app.height)//10
  app.brainHighlight = 'pink'
  app.brainShadow = 'palevioletred3'
  app.brainOutline = 'gray'
  app.page = 'main'
  app.mousePresses = []
  app.buttonColor = 'white'
  app.signal = signal(200, 200)
  app.size = 0
  app.isGameOver = False
  app.timerDelay = 20
  app.moveLorR = False
  app.beamHeight = 2
  app.beamLength = 20
  app.beamColor = 'black'
  app.beams = []
  app.currentKeyPressTimeRight = 0
  app.currentKeyPressTimeLeft = 0
  app.previousY = 200 # check if this works for jumping movement
  app.movementDown = True
  app.yCoordJump = 0
  #app.scrollY = 0
  #app.scrollMargin = 50
  createBeams(app)
  app.obstacleR = 2
  app.obstacles = set()
  app.currentJumpStartTime = 0
  app.jumpUpperBounds = 0
  app.direction = 1
  app.score = -1
  app.scoreList = []
  app.highestY = 0
  app.addObstacle = True
  app.boost = False
  app.boostStartTime = 0
  app.boostLabel = False
  app.randSignal = randSignal(app.margin*2 + 10, app.margin*2 + 10)
  app.signalEntry = None
  app.nameEntry = None

def mousePressed(app, event):
    (x, y) = (event.x, event.y)
    app.mousePresses.append((x,y))
    #for help screen
    xcenter = app.width -0.580*app.margin 
    ycenter = 0.580* app.margin
    x0 = xcenter - 0.4*app.margin
    x1 = xcenter + 0.4*app.margin
    y0 = ycenter - 0.4*app.margin
    y1 = ycenter + 0.4*app.margin

    if app.page == 'main':
       #play button --> choices page
        leftPlay = app.width/2 - app.margin/2
        rightPlay = app.width/2 + app.margin/2
        downPlay = app.height/2 - app.margin/2
        upPlay = app.height/2 + app.margin/2
        for (x, y) in app.mousePresses:
            if x <= rightPlay and x >= leftPlay:
                if y <= upPlay and y >= downPlay:
                  
                    app.page = 'choices' #change to choices
 
                    level = 1
        for x, y in app.mousePresses: 
            if x >= x0 and x <= x1: 
                if y >= y0 and y <= y1: 
                    app.page = 'help'

        app.mousePresses = []
    if app.page == 'lost':
       #go back to main page
        left = app.width/2 - app.margin
        right = app.width/2 + app.margin
        up = app.margin + 0.65*app.margin + app.margin/3
        down = app.margin + 0.65*app.margin - app.margin/3
        for (x, y) in app.mousePresses:
            if x <= right and x >= left:
                if y <= up and y >= down:
                    app.page = 'main'
                    app.level = 1
        for x, y in app.mousePresses: 
            if x >= x0 and x <= x1: 
                if y >= y0 and y <= y1: 
                    app.page = 'help'
       #replay game --> choices page
        app.mousePresses = []
    if app.page == 'win':
       #go back to main page
        left = app.width/2 - app.margin
        right = app.width/2 + app.margin
        up = app.margin + 0.65*app.margin + app.margin/3
        down = app.margin + 0.65*app.margin - app.margin/3
        for (x, y) in app.mousePresses:
            if x <= right and x >= left:
                if y <= up and y >= down:
                    app.page = 'main'
                    app.level = 1
        for x, y in app.mousePresses: 
            if x >= x0 and x <= x1: 
                if y >= y0 and y <= y1: 
                    app.page = 'help'
       #replay game --> choices page
    if app.page == 'choices':
        width = app.width - 4*app.margin
        xDist = width // 6
        r = app.signal.r
        sy = 3.5* app.margin
        for (x , y) in app.mousePresses:
           #blue --> blue
            blueX = 2*app.margin + xDist
            if x >= (blueX - r) and x <= (blueX + r):
                if y >= (sy-r) and y <= (sy+r):
                    app.signal.fill = 'blue'
           #green --> green
            greenX = blueX + xDist
            if x >= (greenX - r) and x <= (greenX + r):
                if y >= (sy-r) and y <= (sy+r):
                    app.signal.fill = 'green'
           #orange --> orange
            orangeX = greenX + xDist
            if x >= (orangeX - r) and x <= (orangeX + r):
                if y >= (sy-r) and y <= (sy+r):
                    app.signal.fill = 'orange'
           #yellow --> yellow
            yellowX = orangeX + xDist
            if x >= (yellowX - r) and x <= (yellowX + r):
                if y >= (sy-r) and y <= (sy+r):
                    app.signal.fill = 'yellow'
           #pink --> pink
            pinkX = yellowX  + xDist
            if x >= (pinkX - r) and x <= (pinkX + r):
                if y >= (sy-r) and y <= (sy+r):
                    app.signal.fill = 'pink'
          
        nWidth = app.width - 2*app.margin
        nxDist = nWidth // 7
        y0 = 6*app.margin
        y1 = 7*app.margin
        x0 = app.margin + nxDist
       #easy
        for (x, y) in app.mousePresses:
            xE = x0 + nxDist
            if x >= x0 and x<= xE:
                if y<=y1 and y>=y0:
                    app.level = 1
            mx0 = x0 + 2*nxDist
            mx1 = mx0 + nxDist
            if x >= mx0 and x<=mx1:
                if y <= y1 and y>= y0:
                    app.level = 2
            hx0 = mx0 + 2*nxDist
            hx1 = hx0 + nxDist
            if x>= hx0 and x<=hx1:
                if y <= y1 and y>=y0:
                    app.level = 3
        for (x,y) in app.mousePresses:
            playX = app.width//2
            nr = app.margin/2
            playY = 8*app.margin
            if x >= (playX - r) and x <= (playX + r):
                if y >= (playY - r) and y <= (playY + r):
                    app.page = 'gameState'
        app.mousePresses = []
        for x, y in app.mousePresses: 
            if x >= x0 and x <= x1: 
                if y >= y0 and y <= y1: 
                    app.page = 'help'
    if app.page == 'gameState':
        left = app.width/2 - app.margin
        right = app.width/2 + app.margin
        up = app.margin + 0.65*app.margin + app.margin/3
        down = app.margin + 0.65*app.margin - app.margin/3
        for (x, y) in app.mousePresses:
            if x <= right and x >= left:
                if y <= up and y >= down:
                    app.page = 'main'
                    app.level = 1
        for x, y in app.mousePresses: 
            if x >= x0 and x <= x1: 
                if y >= y0 and y <= y1: 
                    app.page = 'help'
        app.mousePresses = []
    if app.page == 'help':
        left = app.width/2 - app.margin
        right = app.width/2 + app.margin
        up = app.margin + 0.65*app.margin + app.margin/3
        down = app.margin + 0.65*app.margin - app.margin/3
        for (x, y) in app.mousePresses:
            if x <= right and x >= left:
                if y <= up and y >= down:
                    app.page = 'main'
                    app.level = 1
 
def reachedTheEnd(app):
   if app.beams[-1][2] == True or app.beams[-2][2] == True:
       return True
   return False
        
def keyPressed(app, event):
    if event.key == 'h':
        app.page = 'help'
    if event.key == 'r': #allows you to restart the jumping motion
          appStarted(app)
          app.page = 'choices'
    if app.page != 'main':
        if event.key == 'Space':
            if app.signal == []:
              #ensures there is only one signal per game cycle
                app.signal = signal(200, 150 + app.scrollMargin)
              #app.signal.append(sig)
                app.obstacles = set()
      
          #app.page = 'gameState'
        if event.key == 'Up':
            pass
        if event.key == 'Right':
            app.currentKeyPressTimeRight = app.size
            app.moveLorR = True
        if event.key == 'Left':
            app.currentKeyPressTimeLeft = app.size
            app.moveLorR = True
    elif app.page == 'main': #not even sure what to do here yet
        if event.key in ['Up', 'Right']:
            app.level += 1
        elif event.key in ['Down', 'Left'] and (app.level > 0):
            app.level -= 1


def checkScore(app):
   app.scoreList = copy.copy(app.beams)
   for [leftpixel, toppixel, jumpedYet, obstacle] in app.beams:
       if app.signal.cy < toppixel:
           app.score += 1
           app.scoreList.remove([leftpixel, toppixel, jumpedYet, obstacle])

def timerFired(app):
    app.size += 1
    if app.page == 'gameState':
        if app.isGameOver == False:
            if app.signal.cy > app.beams[0][1]:
                app.page = 'lost'
                app.isGameOver = True
            if canBoost(app):
                app.boostStartTime = app.size
                app.score += 1
                app.boost = True
            if app.boostStartTime + 10 >= app.size:
                app.signal.cy -= 15
                if app.signal.cy <= app.beams[-1][1]:
                    addBeams(app)
                    if app.level < 3:
                        app.level += 1
                    else:
                        app.page = 'win'
                        app.isGameOver = True
                app.boostLabel = True
            else:
                app.boostLabel = False
                app.boost = False
            lastJump = app.beams[-1][2]
            secondToLastJump = app.beams[-2][2]
            if lastJump == True or secondToLastJump == True:
                if app.level == 3:
                   app.page = 'win'
                   app.isGameOver = True
                elif app.level == 1:
                   app.level = 2
                   addBeams(app)
                elif app.level == 2:
                   app.level = 3
                   addBeams(app)
                   app.obstacles = set()
 
            checkSignal(app)
           #OBSTACLES
            if app.level !=1:
                createObstacles(app)
            if app.level == 3: 
               updateRandSignals(app)
               sy = app.signal.cy - app.height/2
               sx = app.signal.cx - app.width/2
            
               app.randSignal.cx += app.randSignal.speedx
               app.randSignal.cy += app.randSignal.speedy
               if signalClashes(app):
                   app.page = 'lost'
                   app.isGameOver = True
           #GRAVITY
            if app.movementDown == True:
               app.signal.cy -= app.gravity
               app.gravity -= 0.02
           #JUMPING
            jump(app)
            if app.movementDown == False:
                app.gravity = -3.2
                if app.signal.cy > app.finalCoordinateJump:
                    if app.signal.cy < app.yCoordJump - 50:
                       app.signal.cy += 0.2*app.velocity
                    elif app.signal.cy < app.yCoordJump - 40:
                       app.signal.cy += 0.3*app.velocity
                    elif app.signal.cy < app.yCoordJump - 30:
                       app.signal.cy += 0.5*app.velocity
                    else:
                       app.signal.cy += app.velocity
                       app.velocity += app.acceleration
                else:
                    app.movementDown = not app.movementDown
                    app.velocity = -18
            app.velocity = -18
            if (app.size % 10) >= 5 and (app.moveLorR == True):
                if app.size % 10 == 9:
                    app.moveLorR = False
 
            if app.size <= app.currentKeyPressTimeRight + 6:
                app.signal.cx += 3
                app.signal.cy +=1.05*app.gravity
            elif app.size > app.currentKeyPressTimeRight + 6:
                app.currentKeyPressTimeRight = 0
            if app.size <= app.currentKeyPressTimeLeft + 6:
              
                app.signal.cx -= 3
                app.signal.cy +=1.05*app.gravity
            elif app.size > app.currentKeyPressTimeLeft + 6:
                app.currentKeyPressTimeLeft = 0
        elif app.isGameOver == True:
            pass
    elif app.page == 'choices':
       pass
    elif app.page == 'lost':
       pass
    elif app.page == 'win':
       pass
    elif app.page == 'main':
       pass
 
def redrawAll(app, canvas):
    x = app.width/2
    y = app.height/2
    
    if app.page == 'main': 
        drawBackground(app, canvas)
        drawHelpButton(app, canvas)
        drawName(app, canvas)
        drawBrain(app, canvas, x, y)
        drawPlayButton(app, canvas)
    elif app.page == 'choices':
        drawBackground(app, canvas)
        #drawHelpButton(app, canvas)
        drawName(app, canvas)
        drawSignalChoices(app, canvas)
        drawGameChoices(app, canvas)
    elif app.page == 'help':
        drawBackground(app, canvas)
        drawHelpButton(app, canvas)
        drawHelpScreen(app, canvas)
        drawName(app, canvas)

    elif app.page == 'lost' or app.page == 'win':
        drawBackground(app, canvas)
        
        drawHelpButton(app, canvas)
        
        drawGameOver(app, canvas)
        drawLittleBrain(app, canvas, 200, 125, 30)
        drawName(app, canvas)
        drawRestart(app, canvas)
    elif app.page == 'gameState':
        drawBackground(app, canvas)
        drawHelpButton(app, canvas)
        drawName(app, canvas)
        drawGamePage(app, canvas)
        drawScore(app, canvas)
        drawLevel(app, canvas)
        if app.level == 1:
            drawBeams(app, canvas)
            drawSignal(app, canvas)
            
        if app.level == 2:
            drawBeams(app, canvas)
            drawObstacle(app, canvas)
            drawSignal(app, canvas)
            
        if app.level == 3:
            drawBeams(app, canvas)
            drawObstacle(app, canvas)
            drawSignal(app, canvas)
            drawRandSignal(app, canvas)
        if app.boostLabel == True:
            drawBoost(app, canvas)


def runNeuroJump():
  print('Running NeuroJump!')
  runApp(width=400, height=400)
runNeuroJump()