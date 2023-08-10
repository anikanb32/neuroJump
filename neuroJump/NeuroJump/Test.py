# 112 Term Project
# Anika Bhagavatula
# Andrew ID: abhagava
import copy
import math
import random
import string
import turtle

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
  # note: use math.isclose() outside 15-112 with Python version 3.5 or later
  return (abs(d2 - d1) < epsilon)
 
import decimal


def roundHalfUp(d): #helper-fn
  # Round to nearest with ties going away from zero.
  rounding = decimal.ROUND_HALF_UP
  # See other rounding options here:
  # https://docs.python.org/3/library/decimal.html#rounding-modes
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
 
def appStarted(app):
  app.gravity = -3.2
  app.acceleration = 3.2
  app.velocity = -18
  app.level = 2
  app.width = 400
  app.height = 400
  app.margin = min(app.width, app.height)//10
  app.brainHighlight = 'pink'
  app.brainShadow = 'palevioletred3' #'burlywood3'
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
  app.previousY = 200 
  #callSignal(app)
  app.movementDown = True
  app.yCoordJump = 0
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
 
###############################################################################
#SIGNAL FUNCTIONS
###############################################################################
def drawLittleBrain(app, canvas, centerx, centery, radius):
    centerx = centerx
    centery = centery
    radius = radius
    magenta = 7
    canvas.create_oval(centerx - radius, centery-radius, centerx + radius, centery + radius, fill = 'thistle2', outline = 'thistle2')
    newcenterx = centerx - 1*radius
    newRadius = 0.75*radius
    canvas.create_oval(newcenterx - newRadius, centery - newRadius, newcenterx + newRadius, centery + newRadius, fill = 'pink', outline = 'pink')
    newcy = centery+5
    newcx = centerx + radius
    canvas.create_oval(newcx - radius, newcy - radius, newcx + radius, newcy + radius, fill = 'pink', outline = 'pink')
    smally = newcy + 0.85*radius
    smallx = newcx - 10
    smallrad = 0.5*radius
    canvas.create_oval(smallx - smallrad, smally - smallrad, smallx + smallrad, smally + smallrad, fill = 'pink', outline = 'pink')
    smallesty = smally + 12
    smallestx = smallx + 6
    smallestrad = 0.55*smallrad
    canvas.create_oval(smallestx - smallestrad, smallesty - smallestrad, smallestx + smallestrad, smallesty + smallestrad, fill = 'pink', outline = 'pink')
    canvas.create_oval(centerx - 0.5*newRadius - radius, centery , centerx + newRadius - radius, centery + newRadius + 0.5*newRadius, fill = 'palevioletred3', outline = 'thistle2', width = 4)
    cx = newcx + 5
    cy = newcy + 10
    rad = 0.35*radius
    canvas.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, outline = 'palevioletred3', width = 4)
    newx = cx - 20
    newy = cy - 20
    radi = 0.7*rad
    canvas.create_oval(newx - radi, newy - radi, newx + radi, newy + radi, fill = 'palevioletred3', outline = 'palevioletred3')
    canvas.create_text(centerx + 5 , centery , text = 'NEUROJump', fill = 'black', font=f'Arial 15 bold')



class randSignal(object):
   def __init__(self, cx, cy):
       self.radius = 5
       self.cx = cx
       self.cy = cy
       self.speedx = 5
       self.speedy = 5
       self.shiftFactor = -1
       self.active = True
      
def updateRandSignals(app):
   sy = app.signal.cy - app.height/2
   sx = app.signal.cx - app.width/2
   x0 = app.randSignal.cx - app.randSignal.radius -sx
   x1 = app.randSignal.cx + app.randSignal.radius -sx
   y0 = app.randSignal.cy - app.randSignal.radius -sy
   y1 = app.randSignal.cy + app.randSignal.radius -sy
   if x1 >= app.width - 2*app.margin:
       app.randSignal.speedx *= app.randSignal.shiftFactor
   elif x0 <= 2*app.margin:
       app.randSignal.speedx *= app.randSignal.shiftFactor
   if y1 >= app.height - 2*app.margin:
       app.randSignal.speedy *= app.randSignal.shiftFactor
   elif y0 <= 2*app.margin:
       app.randSignal.speedy *= app.randSignal.shiftFactor
 
def drawRandSignal(app, canvas):
    sy = app.signal.cy - app.height/2
    sx = app.signal.cx - app.width/2
    x0 = app.randSignal.cx - app.randSignal.radius - sx
    x1 = app.randSignal.cx + app.randSignal.radius - sx
    y0 = app.randSignal.cy - app.randSignal.radius - sy
    y1 = app.randSignal.cy + app.randSignal.radius - sy
    if y0 >= 2*app.margin and y1 <= app.height - 2*app.margin:  
        if x0 >= 2*app.margin and x1 <= app.width - 2*app.margin:  
            canvas.create_oval(x0, y0, x1, y1, fill = 'purple')
 
class signal(object):
  def __init__(self, cx, cy): #add app.margin for y if needed?
      self.cx = cx
      self.cy = cy
      colors = ['red', 'orange', 'blue', 'green']
      self.fill = 'black'
      self.r = 5
 
 

def drawSignal(app, canvas):
  canvas.create_oval(app.width/2 - app.signal.r,
  app.height/2 - app.signal.r, app.width/2 + app.signal.r,
  app.height/2 + app.signal.r, fill = app.signal.fill)
 
def callSignal(app):
  if app.signal == []:
      #ensures there is only one signal per game cycle
      app.signal = signal(200, 150 +  app.scrollMargin)
def checkSignal(app):
  lowerBounds = app.height - 2*app.margin
  upperBounds = 2*app.margin
  leftBounds = 2*app.margin
  rightBounds = app.width - 2*app.margin
  xCoord = app.signal.cx
  yCoord = app.signal.cy
  if yCoord >= lowerBounds or yCoord <= upperBounds:
      #app.signal = []
      return False
  elif xCoord >= rightBounds or xCoord <= leftBounds:
      #app.signal = []
      return False
  return True
 
###############################################################################
# BASIC DRAW FUNCTIONS
###############################################################################
 
def drawBrain(app, canvas, x, y):
    radiusLargeDot = app.margin/2
    radiusMediumDot = app.margin/4
    radiusSmallDot = app.margin/6
    canvas.create_oval(x-radiusLargeDot, y-radiusLargeDot, x+radiusLargeDot,
    y+radiusLargeDot, fill = app.brainHighlight)
    x2 = x + 2*radiusLargeDot
    y2 = y + 2*radiusLargeDot
    canvas.create_oval(x2-radiusLargeDot, y2-radiusLargeDot, x2+radiusLargeDot,
    y2+radiusLargeDot, fill = app.brainHighlight)
    x3 = x - 2*radiusLargeDot
    y3 = y - 2*radiusLargeDot
    canvas.create_oval(x3-radiusLargeDot, y3-radiusLargeDot, x3+radiusLargeDot,
    y3+radiusLargeDot, fill = app.brainHighlight)
    x4 = x + 4*radiusLargeDot
    y4 = y
    canvas.create_oval(x4-radiusLargeDot, y4-radiusLargeDot, x4+radiusLargeDot,
    y4+radiusLargeDot, fill = app.brainShadow)
    x5 = x - 2*radiusLargeDot
    y5 = y
    canvas.create_oval(x5-radiusMediumDot, y5-radiusMediumDot,
    x5+radiusMediumDot, y5+radiusMediumDot, fill = app.brainHighlight)
    x6 = x5 - 1.5*radiusLargeDot
    y6 = y - .75*radiusLargeDot
    canvas.create_oval(x6-radiusMediumDot, y6-radiusMediumDot,
    x6+radiusMediumDot, y6+radiusMediumDot, fill = app.brainShadow)
    x7 = x
    y7 = y - 2*radiusLargeDot
    canvas.create_oval(x7-radiusMediumDot, y7-radiusMediumDot,
    x7+radiusMediumDot, y7+radiusMediumDot, fill = app.brainHighlight)
    x8 = x - radiusMediumDot
    y8 = y7 -1.5*radiusLargeDot
    canvas.create_oval(x8-radiusMediumDot, y8-radiusMediumDot,
    x8+radiusMediumDot, y8+radiusMediumDot, fill = app.brainShadow)
    x9 = x - 3.25*radiusLargeDot
    y9 = y + 0.5*radiusLargeDot
    canvas.create_oval(x9-radiusMediumDot, y9-radiusMediumDot,
    x9+radiusMediumDot, y9+radiusMediumDot, fill = app.brainShadow)
    x10 = x + 2*radiusLargeDot
    y10 = y
    canvas.create_oval(x10-radiusMediumDot, y10-radiusMediumDot,
    x10+radiusMediumDot, y10+radiusMediumDot, fill = app.brainShadow)
    x11 = x
    y11 = y + 2*radiusLargeDot
    canvas.create_oval(x11-radiusMediumDot, y11-radiusMediumDot,
    x11+radiusMediumDot, y11+radiusMediumDot, fill = app.brainHighlight)
    x12 = x2 + radiusLargeDot
    y12 = y2 + 1.5*radiusLargeDot
    canvas.create_oval(x12-radiusMediumDot, y12-radiusMediumDot,
    x12+radiusMediumDot, y12+radiusMediumDot, fill = app.brainHighlight)
    x13 = x12 + 1.75*radiusMediumDot
    y13 = y12 + 1.5*radiusMediumDot
    canvas.create_oval(x13-radiusSmallDot, y13-radiusSmallDot,
    x13+radiusSmallDot, y13+radiusSmallDot, fill = app.brainShadow)
    x14 = x - 2*radiusLargeDot
    y14 = y + 2*radiusLargeDot
    canvas.create_oval(x14-radiusLargeDot, y14-radiusLargeDot,
    x14+radiusLargeDot, y14+radiusLargeDot, fill = app.brainShadow)
    x15 = x2 + 2*radiusLargeDot
    y15 = y2
    canvas.create_oval(x15-radiusMediumDot, y15-radiusMediumDot,
    x15+radiusMediumDot, y15+radiusMediumDot, fill = app.brainHighlight)
    x16 = x15
    y16 = y15 + 2.2*radiusMediumDot
    canvas.create_oval(x16-radiusSmallDot, y16-radiusSmallDot,
    x16+radiusSmallDot, y16+radiusSmallDot, fill = app.brainHighlight)
    x17 = x + 2*radiusLargeDot
    y17 = y - 2*radiusLargeDot
    canvas.create_oval(x17-radiusLargeDot, y17-radiusLargeDot,
    x17+radiusLargeDot, y17+radiusLargeDot, fill = app.brainShadow)
    x18 = x17 + 2*radiusLargeDot
    y18 = y17
    canvas.create_oval(x18-radiusMediumDot, y18-radiusMediumDot,
    x18+radiusMediumDot, y18+radiusMediumDot, fill = app.brainShadow)
    x19 = x17 - 1*radiusLargeDot
    y19 = y17 - 1.5*radiusLargeDot
    canvas.create_oval(x19-radiusSmallDot, y19-radiusSmallDot,
    x19+radiusSmallDot, y19+radiusSmallDot, fill = app.brainHighlight)
    x20 = x17 + 1.25*radiusLargeDot
    y20 = y17 - 1.25*radiusLargeDot
    canvas.create_oval(x20-radiusSmallDot, y20-radiusSmallDot,
    x20+radiusSmallDot, y20+radiusSmallDot, fill = app.brainHighlight)
    x21 = x4 + 1.25*radiusLargeDot
    y21 = y4 + 1.35*radiusLargeDot
    canvas.create_oval(x21-radiusMediumDot, y21-radiusMediumDot,
    x21+radiusMediumDot, y21+radiusMediumDot, fill = app.brainHighlight)
    x22 = x4 + 1.65*radiusLargeDot
    y22 = y4 + .5*radiusSmallDot
    canvas.create_oval(x22-radiusSmallDot, y22-radiusSmallDot,
    x22+radiusSmallDot, y22+radiusSmallDot, fill = app.brainHighlight)
    x23 = x4 + 1.25*radiusLargeDot
    y23 = y4 - 1.25*radiusLargeDot
    canvas.create_oval(x23-radiusMediumDot, y23-radiusMediumDot,
    x23+radiusMediumDot, y23+radiusMediumDot, fill = app.brainHighlight)
    x24 = x9 - .5*radiusLargeDot
    y24 = y9 + 1.2*radiusLargeDot
    canvas.create_oval(x24-radiusMediumDot, y24-radiusMediumDot,
    x24+radiusMediumDot, y24+radiusMediumDot, fill = app.brainHighlight)
    x25 = x24 - .9*radiusLargeDot
    y25 = y24 - 1.2*radiusLargeDot
    canvas.create_oval(x25-radiusMediumDot, y25-radiusMediumDot,
    x25+radiusMediumDot, y25+radiusMediumDot, fill = app.brainHighlight)
    x26 = x25
    y26 = y25 - 1.25*radiusLargeDot
    canvas.create_oval(x26-radiusSmallDot, y26-radiusSmallDot,
    x26+radiusSmallDot, y26+radiusSmallDot, fill = app.brainHighlight)
    x27 = x26 + .75*radiusLargeDot
    y27 = y26 - 1.25*radiusLargeDot
    canvas.create_oval(x27-radiusMediumDot, y27-radiusMediumDot,
    x27+radiusMediumDot, y27+radiusMediumDot, fill = app.brainHighlight)
    x28 = x27 + radiusMediumDot
    y28 = y27 - 1.2*radiusLargeDot
    canvas.create_oval(x28-radiusSmallDot, y28-radiusSmallDot,
    x28+radiusSmallDot, y28+radiusSmallDot, fill = app.brainShadow)
    x29 = x28 + 1.2*radiusLargeDot
    y29 = y28 - .5*radiusLargeDot
    canvas.create_oval(x29-radiusSmallDot, y29-radiusSmallDot,
    x29+radiusSmallDot, y29+radiusSmallDot, fill = app.brainShadow)
 
def drawBackground(app, canvas):
  x1 = app.width - app.margin
  x2 = app.height - app.margin
  canvas.create_rectangle(0,0, app.width, app.height, fill = 'pink')
  canvas.create_rectangle(app.margin, app.margin, x1, x2, fill = 'black')
def drawName(app, canvas):
  x = app.width/2
  y = app.margin/2
  canvas.create_text(x, y, text = 'NEUROJump', fill = 'black', 
   font=f'Arial 15 bold')
def drawPlayButton(app, canvas):
  x = app.width/2
  y = app.height/2
  canvas.create_text(x, y, text = 'Play', font = f'Arial 15 bold')
 
def drawSignalChoices(app, canvas):
   centerxtext = app.width/2
   centerytext = 2.5*app.margin
   canvas.create_text(centerxtext, centerytext, text = 'Choose Signal Color:', 
   fill = 'thistle2', font = f'Arial 15 bold')
   r = app.signal.r
   width = app.width - 4*app.margin
   xDist = width // 6
   blueX = 2*app.margin + xDist
  
   sy = 3.5*app.margin
   #5 color options
   #blue
   canvas.create_oval(blueX - r, sy - r, blueX + r, sy + r, fill = 'blue')
   #green
   greenX = blueX + xDist
   canvas.create_oval(greenX - r, sy - r, greenX + r, sy + r, fill = 'green')
   #orange
   orangeX = greenX + xDist
   canvas.create_oval(orangeX - r, sy - r, orangeX + r, sy + r, fill = 'orange')
   #yellow
   yellowX = orangeX + xDist
   canvas.create_oval(yellowX - r, sy - r, yellowX + r, sy + r, fill = 'yellow')
   #pink
   pinkX = yellowX  + xDist
   canvas.create_oval(pinkX - r, sy - r, pinkX + r, sy + r, fill = 'pink')
  
def drawGameChoices(app, canvas):
   centerxtext = app.width/2
   centerytext = 5*app.margin
   canvas.create_text(centerxtext, centerytext, 
   text = 'Choose Difficulty Level:', fill = 'thistle2', 
   font = f'Arial 15 bold')
 
   width = app.width - 2*app.margin
   xDist = width // 7
   y0 = 6*app.margin
   y1 = 7*app.margin
   x0 = app.margin + xDist
   #easy
   canvas.create_rectangle(x0, y0, x0 + xDist, y1, fill = 'purple')
   y = (y0+y1)/2
   xE = (x0 + x0 + xDist)/2
   canvas.create_text(xE, y, text = 'Easy', fill = 'white')
 
   #medium
   mx0 = x0 + 2*xDist
   canvas.create_rectangle(mx0, y0, mx0 + xDist, y1, fill = 'purple')
   xM = (mx0 + mx0 + xDist)/2
   canvas.create_text(xM, y, text = 'Med', fill = 'white')
   #hard
   hx0 = mx0 + 2*xDist
   canvas.create_rectangle(hx0, y0, hx0 + xDist, y1, fill = 'purple')
   xH = (hx0 + hx0 + xDist)/2
   canvas.create_text(xH, y, text = 'Hard', fill = 'white')
 
 
   playX = app.width //2
   r = app.margin/2
   playY = 8*app.margin
   playDistY = 0.5*app.margin
   canvas.create_oval(playX - r, playY - r, playX + r, playY + r, fill = 'pink')
   canvas.create_text(playX, playY, text = 'Play', fill = 'black', 
   font = f'Arial 15 bold')
 
###############################################################################
# MOUSEPRESSED AND KEYPRESSED (CONTROLLERS)
###############################################################################
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
    else: 
        app.page == 'notAValidPage'
        app.level == 1
 
###############################################################################
# BEAMS
###############################################################################
 
def addBeams(app):
   newBeams = []
   [leftpixel, toppixel, jumpedYet, obstacle] = app.beams[-1]
   yDifference = (app.height - 4*app.margin)//8
   lowerBound = toppixel
   leftBound = 2*app.margin
   rightBound = app.width - 2*app.margin - app.beamLength
   while len(newBeams) < 18:
       leftpixel = random.randint(leftBound, rightBound)
       toppixel = lowerBound - (len(newBeams)*yDifference)
       newBeams.append([leftpixel, toppixel, False, False])
  
   app.beams.extend(newBeams)
 
def drawBeams(app, canvas): #draw has to be with respect to scroll
   sy = app.signal.cy - app.height/2
   sx = app.signal.cx - app.width/2
   for [leftpixel, toppixel, jumpedYet, obstacle] in app.beams:
       y0, y1 = toppixel - sy, toppixel + app.beamHeight - sy
       x0, x1 = leftpixel - sx, leftpixel + app.beamLength -sx
       if y0 < 2*app.margin or y1 > app.height - 2*app.margin:
           continue
       if x1 < 2*app.margin or x0 >app.width - 2*app.margin:
           continue
       canvas.create_rectangle(x0, y0,
       x1, y1,
       fill = app.beamColor)
 

def isLegalBeam(app, L, T):
  currleftpix = L
  currtoppix = T
  for [leftpixel, toppixel, jumpedYet, obstacle] in app.beams:
      if abs(currleftpix - leftpixel) < 10:
          return False
      if abs(currtoppix - toppixel) < 20:
          return False
  return True

 
 
def createBeams(app):
   while len(app.beams) < 18:
       leftBound = 2*app.margin
       rightBound = app.width - 2*app.margin - app.beamLength
       #leftpixel = random.randint(leftBound, rightBound)
       upperBound = 2*app.margin
       # app.level = 1 = 12
       # app.level = 2 = 9
       # app.level = 3 = 6
       if app.level ==  1:
           divisorForDiff = 12
       elif app.level == 2:
           divisorForDiff = 10
       elif app.level == 3:
           divisorForDiff = 9
       if app.level == 3:
           yDifference = (app.height - 4*app.margin)//divisorForDiff
           lowerBound = app.height - 2*app.margin - app.beamHeight
           #toppixel = random.randint(upperBound, lowerBound)
           if len(app.beams) == 0:
               leftpixel = app.width/2 - 0.5*app.beamLength
               toppixel = lowerBound
           else:
               leftpixel = random.randint(leftBound, rightBound)
               toppixel = lowerBound - (len(app.beams)*yDifference)
           if isLegalBeam(app, leftpixel, toppixel):
               #case where adds beam
               app.beams.append([leftpixel, toppixel, False, False])
       elif app.level == 1 or app.level == 2:
           yDifference = (app.height - 4*app.margin)//divisorForDiff
           lowerBound = app.height - 2*app.margin - app.beamHeight
           #toppixel = random.randint(upperBound, lowerBound)
           if len(app.beams) == 0:
               leftpixel = app.width/2 - 0.5*app.beamLength
               toppixel = lowerBound
           else:
               leftpixel = random.randint(leftBound, rightBound)
               secondleftpixel = random.randint(leftBound, rightBound)
               toppixel = lowerBound - (len(app.beams)*yDifference)
               if isLegalHorizontalPixels(app, leftpixel, secondleftpixel):
                   if isLegalBeam(app, leftpixel, toppixel) and isLegalBeam(app,
                    secondleftpixel, toppixel):
                       app.beams.append([leftpixel, toppixel, False, False])
                       app.beams.append([secondleftpixel, toppixel, False,
                        False])
 
           if isLegalBeam(app, leftpixel, toppixel):
               #case where adds beam
               app.beams.append([leftpixel, toppixel, False, False])
 
def isLegalHorizontalPixels(app, leftpixel, secondleftpixel):
   if abs(leftpixel - secondleftpixel) > app.beamLength + 5:
       return True
   return False
 
###############################################################################
# OBSTACLE
###############################################################################
def canBoost(app):
   if app.score % 5 == 0 and app.score != 0:
       app.boost = True
       return True
   else:
       app.boost = False
       return False
 
class obstacle(object):
  def __init__(self, cx, cy):
      self.cx = cx
      self.cy = cy
      self.fill = 'red'
      self.r = 5
def calcDistance(x0, y0, x1, y1):
   xdist = x1 - x0
   ydist = y1 - y0
   return (xdist**2 + ydist**2)**0.5
 
def determineObstaclePosition(app): #ai algorithm - (original - not used)
   #goal is to find closest beam distance wise (for the jump)
   if app.addObstacle:
       if len(app.obstacles) < 8:
           currentBeam = []
           for i in range(len(app.beams)-1, -1, -1):
               beam = app.beams[i]
               jumpedYet = beam[2]
               if jumpedYet:
                   currentBeam = beam
                   possibleBeamsToAddObstacles = app.beams[i:] #all beams above
                   break
           smallestDist = 400
           bestObstacleBeam = []
           if currentBeam != []:
               [currleftpixel, currtoppixel, 
               currjumpedYet, currobs] = currentBeam
               currcx = currleftpixel + 0.5*app.beamLength
               currcy = currtoppixel - 0.5*app.beamHeight
               for possibleBeam in possibleBeamsToAddObstacles:
                   [possleftpixel, posstoppixel, 
                   possjumpedYet, possobstacle] = possibleBeam
                   posscx = possleftpixel + 0.5*app.beamLength
                   posscy = posstoppixel - 0.5*app.beamHeight
                   dist = calcDistance(currcx, currcy, posscx, posscy)
                   if dist <= smallestDist and dist != 0:
                       smallestDist = dist
                       bestObstacleBeam = possibleBeam
           elif currentBeam == []:
               return
           if bestObstacleBeam != []:
               [leftpix, toppix, jumped, obs] = bestObstacleBeam
               app.obstacles.add((leftpix, toppix))
               for currBeam in app.beams:
                   if currBeam[0] == leftpix and currBeam[1] == toppix:
                       currBeam[3] = True
               currIndex = app.beams.index([leftpix, toppix, False, True])
               if app.beams[1][3] == True:
                   app.obstacles.remove((leftpix, toppix))
                   app.beams[1][3] = False
 
 
               if app.beams[currIndex-1][3] == True:
                   app.obstacles.remove((leftpix, toppix))
                   app.beams[currIndex][3] = False
 
def isLegalObstacle(app):
   obstacleExistence = [[0]*len(app.beams)]
   for beam in app.beams:
 
       pass
 
def drawObstacle(app, canvas):
   sy = app.signal.cy - app.height/2
   sx = app.signal.cx - app.width/2
   #determine whether to draw obstacle first !!! ADD SOMETHIGN HERE
   for position in app.obstacles:
       (leftpixel, toppixel) = position
       y0, y1 = toppixel - sy, toppixel - 2*app.beamHeight - sy
       x0, x1 = (leftpixel - sx + 0.25*app.beamLength , 
       leftpixel + 0.5*app.margin - sx - 0.25*app.beamLength)
       if y1 < 2*app.margin or y0 > app.height - 2*app.margin:
           continue
       if x0 < 2*app.margin or x1 > app.width - 2*app.margin:
           continue
       """ cx = leftpixel + 0.5*app.beamLength
       cy = toppixel - 2*app.beamHeight #this is 2 """
       canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
def obstacleCollision(app): # lose lives if you hit obstacle
  for position in app.obstacles:
      if position != None:
          [leftpixel, toppixel, jumpedYet, obstacle] = position
          cx = leftpixel + 0.5*app.beamLength
          cy = toppixel - 2*app.beamHeight #this is 2
        
          if app.signal.cx in range(leftpixel,
          int(leftpixel + app.beamLength + 1)):
            
              if (app.signal.cy + app.signal.r) in range(
              toppixel - int(1.5*app.beamHeight), toppixel):
                   #HERE IS THE ISSUE
              #game over - change app.isGameOver
                  #app.signal = []
                  app.beams = []
                  app.obstacles = set()
                  createBeams(app)

def drawRestart(app, canvas):
    label = "Press 'R' to Restart"
    x = app.width //2 
    y = app.height - 0.5*app.margin
    canvas.create_text(x, y, text = label, fill = 'palevioletred3', 
    font = 'Arial 11 bold')

def drawBoost(app, canvas):
   width = app.width
   height = app.height
   canvas.create_text(width//2, height//2 + app.margin, text = 'BOOST!', 
   fill = 'white', 
   font = f'Arial 16 bold')

def drawHelpScreen(app, canvas):
    middleX = app.width//2
    middleY = app.height//2
    distanceY = app.margin/3
    distanceX = app.margin
    xCenter = app.width/2
    yCenter = app.margin + 0.5*app.margin
    canvas.create_rectangle(xCenter - distanceX, yCenter - distanceY,
    xCenter + distanceX, yCenter + distanceY, fill = 'palevioletred3')
    canvas.create_text(xCenter, yCenter, text = 'Main Page', 
    font = f'Arial 14 bold')
    canvas.create_text(middleX, app.margin*2.75, text = "Rules", 
    fill = 'pink', font = f'Arial 30 bold')
    canvas.create_text(middleX, app.margin*4, 
    text = '~ Use Left and Right Arrow Keys to Move', fill = 'white', 
    font = f'Arial 12')
    canvas.create_text(middleX, app.margin*5, 
    text = '~ Avoid Red Obstacles on Beams and Purple Signal', fill = 'white', 
    font = f'Arial 12')
    canvas.create_text(middleX, app.margin*6, 
    text = '~ Boost Each Time you Earn 5 Points ', fill = 'white', 
    font = f'Arial 12')
    canvas.create_text(middleX, app.margin*6.5, 
    text = 'From Jumping on Beams', fill = 'white', font = f'Arial 12')
    canvas.create_text(middleX, app.margin*7.5, 
    text = '~ Complete All Levels to Successfully', fill = 'white', 
    font = f'Arial 12')
    canvas.create_text(middleX, app.margin*8, 
    text = 'Pass the Signal to the End of the Neuron!', fill = 'white', 
    font = f'Arial 12')

def drawHelpButton(app, canvas):
    xcenter = app.width -0.580*app.margin 
    ycenter = 0.580* app.margin
    x0 = xcenter - 0.4*app.margin
    x1 = xcenter + 0.4*app.margin
    y0 = ycenter - 0.4*app.margin
    y1 = ycenter + 0.4*app.margin
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'gray', outline = 'gray')
    canvas.create_text(xcenter, ycenter, text = 'Help', fill = 'thistle2', 
    font = f'Arial 13 bold')





###############################################################################
# REDRAW ALL
###############################################################################
 
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
            print('boosting should be')
            drawBoost(app, canvas)


 
 
def shouldJump(app):
  if app.movementDown == True:
      for beam in app.beams:
          [leftpixel, toppixel, jumpedYet, obstacle] = beam
 
          if abs((app.signal.cy + app.signal.r) - toppixel) < 3:
              if ((app.signal.cx) >= leftpixel):
                  if ((app.signal.cx)<= (leftpixel + app.beamLength)):
                       """ for beam in app.beams:
                           if beam[2]:
                               app.highestY = beam[1] """
                       if obstacle == True:
                          
                           app.page = 'lost'
                           app.isGameOver = True
                          
                       if jumpedYet == False: # and app.highestY > toppixel:
                          app.score += 1
                          beam[2] = True
 
                       return True
  return False
 
def drawGameOver(app, canvas):
  
   cx = app.width/2
   cy = app.height/2
 
   if app.isGameOver and app.page == 'lost':
      
       drawBackground(app, canvas)
       canvas.create_text(cx, cy, text = 'Game Over', fill = 'white', 
       font = f'Arial 30 bold')
       canvas.create_text(cx, cy+50, 
       text = 'Sorry You Could Not Pass The Signal...', fill = 'white', 
       font = f'Arial 12')
       canvas.create_text(cx, cy+100, text = f'Final Score = {app.score}', 
       fill = 'white', font = f'Arial 12')
       distanceY = app.margin/3
       distanceX = app.margin
       xCenter = app.width/2
       yCenter = app.margin + 0.5*app.margin
       canvas.create_rectangle(xCenter - distanceX, yCenter - distanceY,
       xCenter + distanceX, yCenter + distanceY, fill = 'palevioletred3')
       canvas.create_text(xCenter, yCenter, text = 'Main Page', 
       font = f'Arial 14 bold')
   if app.isGameOver and app.page == 'win':
      
       drawBackground(app, canvas)
       canvas.create_text(cx, cy, text = 'Game Over', fill = 'white', 
       font = f'Arial 30 bold')
       canvas.create_text(cx, cy+50, text = 'SYNAPSE, You Passed The Signal!', 
       fill = 'thistle2', font = f'Arial 15 bold')
       canvas.create_text(cx, cy+100, text = f'Final Score = {app.score}', 
       fill = 'white', font = f'Arial 12')
       distanceY = app.margin/3
       distanceX = app.margin
       xCenter = app.width/2
       yCenter = app.margin + 0.5*app.margin
       canvas.create_rectangle(xCenter - distanceX, yCenter - distanceY,
       xCenter + distanceX, yCenter + distanceY, fill = 'palevioletred3')
       canvas.create_text(xCenter, yCenter, text = 'Main Page', 
       font = f'Arial 14 bold')
 
 
def drawScore(app, canvas):
   cx = app.width//4
   cy = app.height - 0.5*app.margin
   canvas.create_text(cx, cy, text = f'Score = {app.score}', fill = 'black',
   font = f'Arial 12 bold' )
 
def drawLevel(app, canvas):
   cx = 3*(app.width//4)
   cy = app.height - 0.5*app.margin
   canvas.create_text(cx, cy, text = f'Level = {app.level}', fill = 'black', 
   font = f'Arial 12 bold')
 
def changeMovingDirection(app):
   if (app.movementDown == False) and (app.yCoordJump - 50 <= app.signal.cy):
          app.movementDown = True
def jump(app):
  if shouldJump(app):
      app.yCoordJump = app.signal.cy
      app.movementDown = False
      app.finalCoordinateJump = app.yCoordJump - 60
 
def checkScore(app):
   app.scoreList = copy.copy(app.beams)
   for [leftpixel, toppixel, jumpedYet, obstacle] in app.beams:
       if app.signal.cy < toppixel:
           app.score += 1
           app.scoreList.remove([leftpixel, toppixel, jumpedYet, obstacle])
def createBeamGraph(app):
   maxDist = 50
   beamGraph = dict()
   for ind in range(len(app.beams)):
       leftpixel = app.beams[ind][0]
       toppixel = app.beams[ind][1]
       neighbors = list()
       for i in range(ind+1, len(app.beams)):
           neighborleftpixel = app.beams[i][0]
           neighbortoppixel = app.beams[i][1]
           neighborDistance = calcDistance(leftpixel, toppixel, 
           neighborleftpixel, neighbortoppixel)
           if neighborDistance <= maxDist:
               neighbors.append((i, neighborDistance))
       beamGraph[ind] = neighbors
   return beamGraph
 
def bfs(app, beamGraph): # this is ai algorithm used to find best path
   idealPath = []
   for keyIndex in beamGraph:
       #beamGraph[keyIndex] is a set
       maxDist = 50
       bestBeamIndex = None
       for indexDist in beamGraph[keyIndex]:
           #beamGraph[keyIndex][indexDist] is a tuple
          
           if len(beamGraph[keyIndex]) != 0:
               neighborIndex = indexDist[0]
               neighborDistance = indexDist[1]
               if neighborDistance < maxDist:
                   maxDist = neighborDistance
                   bestBeamIndex = neighborIndex
                  
           if bestBeamIndex != None:
               idealPath.append(app.beams[bestBeamIndex])
  
   return idealPath
 
def createObstacles(app): # this is used to make the obstacles
    beamGraph = createBeamGraph(app)
    idealPath = bfs(app, beamGraph) #returns beams that should have obstacle
    for beam in idealPath:
        [leftpixel, toppixel, jumpedYet, obstacleExists] = beam
        centerx = leftpixel + 0.5*app.beamLength
        centery = toppixel + 0.5*app.beamHeight
        app.obstacles.add((leftpixel, toppixel))
        for obsBeam in app.beams:
            if obsBeam[0] == leftpixel and obsBeam[1] == toppixel:
                obsBeam[3] = True
            currIndex = app.beams.index(beam)
            if app.beams[1][3] == True: #second beam shouldnt have obstacle
                app.obstacles.remove((leftpixel, toppixel))
                app.beams[1][3] = False
                if app.beams[currIndex-1][3] == True:
                    app.obstacles.remove((leftpixel, toppixel))
                    app.beams[currIndex][3] = False 
              

def signalClashes(app):
    sigx0 = app.signal.cx - app.signal.r
    sigx1 = app.signal.cx + app.signal.r
    sigy0 = app.signal.cy - app.signal.r
    sigy1 = app.signal.cy + app.signal.r
    crashx0 = app.randSignal.cx - app.randSignal.radius
    crashx1 = app.randSignal.cx + app.randSignal.radius
    crashy0 = app.randSignal.cy - app.randSignal.radius
    crashy1 = app.randSignal.cy + app.randSignal.radius
    xRangeCrash = crashx1 - crashx0
    yRangeCrash = crashy1 - crashy0
    if sigx1 >= crashx0 and sigx1 <= crashx1: 
        #signal crashes with enemy on right and above
        if sigy0 <= crashy1 and sigy0 >= crashy0: 
            return True

        #signal crashes with enemy on right and below
        if sigy1 >= crashy0 and sigy1 <= crashy1:
            return True
    elif sigx0 <= crashx1 and sigx0 >= crashx0: 
        #signal crashes with enemy on left and above
        if sigy0 <= crashy1 and sigy0 >= crashy0: 
            return True

        #signal crashes with enemy on left and below
        if sigy1 >= crashy0 and sigy1 <= crashy1:
            return True
    return False



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
                   #createBeams(app)
                   #app.obstacles = set()
                elif app.level == 2:
                   app.level = 3
                   addBeams(app)
                   #app.beams = []
                   #createBeams(app)
                   app.obstacles = set()
 
            checkSignal(app)
           #checkScore(app)
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

               """ if abs(app.randSignal.cy - app.signal.cy) > 50:
                   app.randSignal.cy -= 10 """
 
              
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
      
#project 2 
#NeuroMap
#need 3d graphics 
#need to do webscraping
#need to implement ai 
# componentsL
# visual map of brain areas (can see what parts of brain are named and highlighted)
# can click on parts of the brain that interested in











def drawGamePage(app, canvas):
  canvas.create_rectangle(2*app.margin, 2*app.margin,
  app.width-2*app.margin, app.height-2*app.margin, fill = 'gray')
  distanceY = app.margin/3
  distanceX = app.margin
  xCenter = app.width/2
  yCenter = app.margin + 0.5*app.margin
  canvas.create_rectangle(xCenter - distanceX, yCenter - distanceY,
  xCenter + distanceX, yCenter + distanceY, fill = 'palevioletred3')
  canvas.create_text(xCenter, yCenter, text = 'Main Page', 
  font = f'Arial 14 bold')
def runNeuroJump():
  print('Running NeuroJump!')
  runApp(width=400, height=400)
runNeuroJump()

 
 
 

