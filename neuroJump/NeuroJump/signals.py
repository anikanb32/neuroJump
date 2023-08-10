

# Signals
#from main import *
from obstacle import *
from signals import *
from draw import *
from cmu_112_graphics import *
import decimal
import random
import copy
from allbeams import *


      
def updateRandSignals(app):
    sy = app.signal.cy - app.height/2
    sx = app.signal.cx - app.width/2
    x0 = app.randSignal.cx - app.randSignal.radius -sx
    x1 = app.randSignal.cx + app.randSignal.radius -sx
    y0 = app.randSignal.cy - app.randSignal.radius -sy
    y1 = app.randSignal.cy + app.randSignal.radius -sy 
    new = 2; 
    if x1 >= app.width - 2*app.margin :
        app.randSignal.speedx *= app.randSignal.shiftFactor
    elif x0  <= 2*app.margin :
        app.randSignal.speedx *= app.randSignal.shiftFactor
    if y1 >= app.height - 2*app.margin:
        app.randSignal.speedy *= app.randSignal.shiftFactor
    elif y0  <= 2*app.margin:
        app.randSignal.speedy *= app.randSignal.shiftFactor
 
#def callSignal(app):
    #if app.signal == []:
        #ensures there is only one signal per game cycle
        #app.signal = signal(200, 150 +  app.scrollMargin)

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
