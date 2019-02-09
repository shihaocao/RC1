import matplotlib.pyplot as plt
import math
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm
import numpy

#distance between points
def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

#creates obstacles
def createObstacle(center, radius):
    deltaT = radius * 4 / 100
    newPointsX = [((radius) * math.cos(theta / deltaT) + center[0]) for theta in range(int(deltaT * 2 * math.pi))]
    newPointsY = [((radius) * math.sin(theta / deltaT) + center[1]) for theta in range(int(deltaT * 2 * math.pi))]
    return (newPointsX, newPointsY)

#waypoints on flight path
currentFlight = [[200, 200], [425, 425]]
planeX = [x for [x, y] in currentFlight]
planeY = [y for [x, y] in currentFlight]
originalX = [x for [x, y] in currentFlight]
originalY = [y for [x, y] in currentFlight]

#creating obstacles
obstacles = [[[300, 350], 100]]
obstacleX = []
obstacleY = []
for center, radius in obstacles:
    oX, oY = createObstacle(center, radius)
    obstacleX.extend(oX)
    obstacleY.extend(oY)

#Plotting stuff
plt.plot(originalX, originalY, 'yo')
plt.plot(planeX, planeY, 'ro')
plt.plot(obstacleX, obstacleY, 'bo')
plt.axis([0, 1000, 0, 1000])
plt.show()

def goAround(obs):

    dist = None
    print(dist)
