

#beams

import random 
#from main import *
from obstacle import *
from signals import *
from draw import *
from cmu_112_graphics import *
import decimal
import copy

def addBeams(app):
    newBeams = []
    [leftpixel, toppixel, jumpedYet, obstacle] = app.beams[-1]
    yDifference = (app.height - 4*app.margin)//10
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

#starting game boolean
#sig.cx and sig.cy - calculate the center of ledge
#exact y coordinates - but x coordinate can be in the range of rectangle
# if ball moves
#jumping is very buggy
def isLegalBeam(app, L, T):
    currleftpix = L
    currtoppix = T
    for [leftpixel, toppixel, jumpedYet, obstacle] in app.beams:
        if abs(currleftpix - leftpixel) < 10:
            return False
        if abs(currtoppix - toppixel) < 20:
            return False
    return True
  #draw beam only if there are certain number on screen
  #draw if there is no overlap of a certain amount
 

def createBeams(app):
    while len(app.beams) < 18:
        leftBound = 2*app.margin
        rightBound = app.width - 2*app.margin - app.beamLength
        upperBound = 2*app.margin
       # app.level = 1 = 12
       # app.level = 2 = 9
       # app.level = 3 = 6
        if app.level ==  1:
            divisorForDiff = 114
        elif app.level == 2:
           divisorForDiff = 12
        elif app.level == 3:
           divisorForDiff = 10
        if app.level == 3:
            yDifference = (app.height - 4*app.margin)//divisorForDiff
            lowerBound = app.height - 2*app.margin - app.beamHeight
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
                    if (isLegalBeam(app, leftpixel, toppixel) and 
                    isLegalBeam(app, secondleftpixel, toppixel)):
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

def shouldJump(app):
    if app.movementDown == True:
        for beam in app.beams:
            [leftpixel, toppixel, jumpedYet, obstacle] = beam
            if abs((app.signal.cy + app.signal.r) - toppixel) < 3:
                if ((app.signal.cx) >= leftpixel):
                    if ((app.signal.cx)<= (leftpixel + app.beamLength)):
                        if obstacle == True:
                            app.page = 'lost'
                            app.isGameOver = True
                        if jumpedYet == False: # and app.highestY > toppixel:
                            app.score += 1
                            beam[2] = True
                        return True
    return False

def changeMovingDirection(app):
    if (app.movementDown == False) and (app.yCoordJump - 50 <= app.signal.cy):
            app.movementDown = True
def jump(app):
    if shouldJump(app):
        app.yCoordJump = app.signal.cy
        app.movementDown = False
        app.finalCoordinateJump = app.yCoordJump - 60