import matplotlib.pyplot as plt
import math
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm
import numpy
#Constants
CHECK_BUFFER = 50
PATH_BUFFER = 80
scale = 100

def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))

def createObstacle(center,radius):
    deltaT = radius*4/100
    newPointsX = [((radius)*math.cos(theta/deltaT) + center[0]) for theta in range(int(deltaT*2*math.pi))]
    newPointsY = [((radius)*math.sin(theta/deltaT) + center[1]) for theta in range(int(deltaT*2*math.pi))]
    return (newPointsX,newPointsY)

def goAroundObstacle(start,end,center,radius,clockwise):
    #Step is constant for waypoint angular distance
    step = radius*math.pi*100/(1000*scale)
    newPathX = []
    newPathY = []

    theta = None
    end_angle = None
    if center[0] == start[0]:
        if start[1] < center[1]:
            theta = 3*math.pi/2
        else:
            theta = math.pi/2
    else:
        theta = math.atan((center[1]-start[1])/(center[0]-start[0]))
        if center[0] - start[0] > 0:
            theta += math.pi
        if theta < 0:
            theta += math.tau

    if center[0] == end[0]:
        if end[1] < center[1]:
            end_angle = 3*math.pi/2
        else:
            end_angle = math.pi/2
    else:
        end_angle = math.atan((center[1]-end[1])/(center[0]-end[0]))
        if center[0] - end[0] > 0:
            end_angle += math.pi
        if end_angle < 0:
            end_angle += math.tau

#    print(theta,end_angle)
    if not clockwise:
        step *= -1
        if end_angle > theta:
            theta += math.tau
        while theta >= end_angle:
            newPathX.append((radius+PATH_BUFFER)*math.cos(theta) + center[0])
            newPathY.append((radius+PATH_BUFFER)*math.sin(theta) + center[1])
            theta += step
    else:
        if end_angle < theta:
            end_angle += math.tau
        while theta <= end_angle:
            newPathX.append((radius+PATH_BUFFER)*math.cos(theta) + center[0])
            newPathY.append((radius+PATH_BUFFER)*math.sin(theta) + center[1])
            theta += step

    return newPathX,newPathY

def self_norm(A):
    return numpy.sqrt(A.dot(A))

def line_point_distance(A1, B1, P1):
    """ segment line AB, point P, where each one is an array([x, y]) """
    A = numpy.array(A1)
    B = numpy.array(B1)
    P = numpy.array(P1)
    if all(A == P) or all(B == P):
        return 0
    temp = dot((P - A) / self_norm(P - A), (B - A) / self_norm(B - A))
    #Math errors, sometimes it becomes 1.000000000002
    if temp < -1:
        temp = -1
    elif temp > 1:
        temp = 1
    if arccos(temp) > pi / 2:
        return norm(P - A)
    temp = dot((P - B) / self_norm(P - B), (A - B) / self_norm(A - B))
    if temp < -1:
        temp = -1
    elif temp > 1:
        temp = 1
    if arccos(temp) > pi / 2:
        return self_norm(P - B)
    return self_norm(cross(A-B, A-P))/self_norm(B-A)

def checkCollision(p, q, center, radius):
    dist = line_point_distance(p,q,center)
#    print(dist)
    if radius + CHECK_BUFFER >= dist:
        return True
    return False

def detectObstaclesInPath(flightPath,obstacles):
    for i in range(len(flightPath)-1):
        for j in range(len(obstacles)):
            center,radius = obstacles[j]
            if checkCollision(flightPath[i],flightPath[i+1],center,radius):
                return i,obstacles[j]
    return None,None

def decideDirection(start,end,center):
    clockwise = True
    if end[0] == start[0] or start[0] == end[0] or end[0] == center[0]:
        if center[0] - end[0] > 0:
            clockwise = False
        else:
            clockwise = True
    else:
        first = start
        second = end
        if start[1] > end[1]:
            first = end
            second = start

        dy_firstCircle = center[1]-first[1]
        dx_firstCircle = center[0]-first[0]
        if second[0]-first[0] > 0 and center[0]-first[0] < 0:
            clockwise = True
        elif second[0]-first[0] < 0 and center[0]-first[0] > 0:
            clockwise = False
        else:
            slope_firstCircle = (dy_firstCircle)/(dx_firstCircle)
            slope_firstSecond = (second[1]-first[1])/(second[0]-first[0])
            if slope_firstCircle > slope_firstSecond:
                clockwise = True
            else:
                clockwise = False
    if start[1] > end[1]:
        return not clockwise
    return clockwise




#Initializing the plane waypoints
currentFlight = [[a*40,a*40] for a in range(25)]

planeX = [x for [x,y] in currentFlight]
planeY = [y for [x,y] in currentFlight]
originalX = [x for [x,y] in currentFlight]
originalY = [y for [x,y] in currentFlight]

obstacles = [[[300,300],100], [[500,500],60]]#[[700,400],150], [[200,600],120]]
obstacleX = []
obstacleY = []
for center,radius in obstacles:
    oX,oY = createObstacle(center,radius)
    obstacleX.extend(oX)
    obstacleY.extend(oY)

index,obstacle = detectObstaclesInPath(currentFlight,obstacles)
count = 0
while index != None and count < 10:
    center,radius = obstacle

    startIndex = index
    endIndex = index+1
    #Find the end waypoint (first waypoint exits obstacle)
    while distance(currentFlight[endIndex][0], currentFlight[endIndex][1], center[0], center[1]) <= radius + PATH_BUFFER:
        endIndex += 1
        if endIndex == len(currentFlight) - 1:
            break

    start = currentFlight[startIndex]
    end = currentFlight[endIndex]

    #Decide whether to go clockwise or counterclockwise (whichever one is shorter)
    clockwise = decideDirection(start,end,center)
    print(clockwise)
    newFlightX,newFlightY = goAroundObstacle(start,end,center,radius,clockwise)
    planeX[startIndex:endIndex] = newFlightX
    planeY[startIndex:endIndex] = newFlightY
    currentFlight = [[planeX[i],planeY[i]] for i in range(len(planeX))]
    index,obstacle = detectObstaclesInPath(currentFlight,obstacles)
#    print(index,currentFlight[index],obstacle)
    count += 1


#Plotting stuff
plt.plot(originalX,originalY,'yo')
plt.plot(planeX,planeY,'ro')
plt.plot(obstacleX,obstacleY, 'bo')
#plt.plot(newPathX,newPathY, 'yo')


plt.axis([0, 1000, 0, 1000])
plt.show()
