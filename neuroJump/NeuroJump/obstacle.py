
#obstacles

#from main import *
from obstacle import *
from signals import *
from draw import *
from cmu_112_graphics import *
import decimal
import random
import copy
from allbeams import *

def canBoost(app):
    if app.score % 5 == 0 and app.score != 0:
        app.boost = True
        return True
    else:
        app.boost = False
        return False
      
 
 

def calcDistance(x0, y0, x1, y1):
   xdist = x1 - x0
   ydist = y1 - y0
   return (xdist**2 + ydist**2)**0.5
 
def determineObstaclePosition(app): #ai algorithm - based on dijkstras algorithm
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
def obstacleCollision(app): # lose if you hit obstacle
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
 
def bfs(app, beamGraph):
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
 
def createObstacles(app):
    beamGraph = createBeamGraph(app)
    idealPath = bfs(app, beamGraph) #returns beams that should have obstacles
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

