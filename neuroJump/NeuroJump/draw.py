
#draw
#from main import *
from obstacle import *
from signals import *
from allbeams import *
from cmu_112_graphics import *
import decimal
import random
import copy

def drawLittleBrain(app, canvas, centerx, centery, radius):
    centerx = centerx
    centery = centery
    radius = radius
    magenta = 7
    canvas.create_oval(centerx - radius, centery-radius, centerx + radius, 
    centery + radius, fill = 'thistle2', outline = 'thistle2')
    newcenterx = centerx - 1*radius
    newRadius = 0.75*radius
    canvas.create_oval(newcenterx - newRadius, centery - newRadius, 
    newcenterx + newRadius, centery + newRadius, fill = 'pink', 
    outline = 'pink')
    newcy = centery+5
    newcx = centerx + radius
    canvas.create_oval(newcx - radius, newcy - radius, newcx + radius, 
    newcy + radius, fill = 'pink', outline = 'pink')
    smally = newcy + 0.85*radius
    smallx = newcx - 10
    smallrad = 0.5*radius
    canvas.create_oval(smallx - smallrad, smally - smallrad, smallx + smallrad, 
    smally + smallrad, fill = 'pink', outline = 'pink')
    smallesty = smally + 12
    smallestx = smallx + 6
    smallestrad = 0.55*smallrad
    canvas.create_oval(smallestx - smallestrad, smallesty - smallestrad, 
    smallestx + smallestrad, smallesty + smallestrad, fill = 'pink', 
    outline = 'pink')
    canvas.create_oval(centerx - 0.5*newRadius - radius, centery , 
    centerx + newRadius - radius, centery + newRadius + 0.5*newRadius, 
    fill = 'palevioletred3', outline = 'thistle2', width = 4)
    cx = newcx + 5
    cy = newcy + 10
    rad = 0.35*radius
    canvas.create_oval(cx - rad, cy - rad, cx + rad, cy + rad, 
    outline = 'palevioletred3', width = 4)
    newx = cx - 20
    newy = cy - 20
    radi = 0.7*rad
    canvas.create_oval(newx - radi, newy - radi, newx + radi, newy + radi, 
    fill = 'palevioletred3', outline = 'palevioletred3')
    canvas.create_text(centerx + 5 , centery , text = 'NEUROJump', 
    fill = 'black', font=f'Arial 15 bold')

def drawRestart(app, canvas):
    label = "Press 'R' to Restart"
    x = app.width //2 
    y = app.height - 0.5*app.margin
    canvas.create_text(x, y, text = label, fill = 'palevioletred3', 
    font = 'Arial 11 bold')

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
    canvas.create_oval(orangeX - r, sy - r, orangeX + r, sy + r, 
    fill = 'orange')
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
    canvas.create_oval(playX - r, playY - r, playX + r, playY + r, 
    fill = 'pink')
    canvas.create_text(playX, playY, text = 'Play', fill = 'black', 
    font = f'Arial 15 bold')


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
    text = '~ Avoid Red Obstacles on Beams and Purple Signal', 
    fill = 'white', font = f'Arial 12')
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

def drawBoost(app, canvas):
    width = app.width
    height = app.height
    canvas.create_text(width//2, height//2 + app.margin, text = 'BOOST!', 
    fill = 'white', font = f'Arial 16 bold')

def drawSignal(app, canvas):
    canvas.create_oval(app.width/2 - app.signal.r,
    app.height/2 - app.signal.r, app.width/2 + app.signal.r,
    app.height/2 + app.signal.r, fill = app.signal.fill)

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
 