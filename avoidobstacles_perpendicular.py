import matplotlib.pyplot as plt
import math
from numpy import arccos, array, dot, pi, cross
from numpy.linalg import det, norm
import numpy

BUFFER = 25
#distance between points
def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

#creates obstacles
def createObstacle(center, radius):
    deltaT = radius * 4 / 100
    newPointsX = [((radius) * math.cos(theta / deltaT) + center[0]) for theta in range(int(deltaT * 2 * math.pi))]
    newPointsY = [((radius) * math.sin(theta / deltaT) + center[1]) for theta in range(int(deltaT * 2 * math.pi))]
    return (newPointsX, newPointsY)

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

def getCircleLineIntersectionPoint(pointA, pointB, center, radius):
    baX = pointB[0] - pointA[0]
    baY = pointB[1] - pointA[1]
    caY = center[1] - pointA[1]
    caX = center[0] - pointA[0]

    a = baX * baX + baY * baY;
    bBy2 = baX * caX + baY * caY;
    c = caX * caX + caY * caY - radius * radius;
    pBy2 = bBy2 / a;
    q = c / a;

    disc = pBy2 * pBy2 - q;
    if disc < 0:
        return []

    tmpSqrt = math.sqrt(disc);
    abScalingFactor1 = -1 * pBy2 + tmpSqrt;
    abScalingFactor2 = -1 * pBy2 - tmpSqrt;
    p1 = [pointA[0] - baX * abScalingFactor1, pointA[1] - baY * abScalingFactor1]
    if disc == 0:
        return [p1];
    p2 = [pointA[0] - baX * abScalingFactor2, pointA[1] - baY * abScalingFactor2]
    return [p1,p2];

def slopeToAngle(dX, dY):
    angle = 0
    if dX == 0:
        if dY > 0:
            angle = math.pi/2
        else:
            angle = 3*math.pi/2
    else:
        angle = math.atan(dY/dX)
        if dX < 0:
            angle += math.pi
    return angle

def goAround(flight,obstacles,iteration,prev_angle = None):
#    print(flight)
    prev = None
    count = 0
    curr_angle = None
    while count < len(flight):
        print(flight)
        [x,y] = flight[count]
        if prev == None:
            prev = [x,y]
            count += 1
            continue
        curr_angle = slopeToAngle(x-prev[0],y-prev[1])
        for [center,radius] in obstacles:
            intersection = getCircleLineIntersectionPoint(prev,[x,y],center,radius+BUFFER)
            newIntersection = []
            for [a,b] in intersection:
                if x < prev[0]:
                    if a >= x and a <= prev[0]:
                        newIntersection.append([a,b])
                else:
                    if a <= x and a >= prev[0]:
                        newIntersection.append([a,b])
            intersection = newIntersection
            if len(intersection) == 0:
                continue
            newPoint = []
            if len(intersection) == 1:
                point = intersection[0]
                dXCenter = point[0] - center[0]
                dYCenter = point[1] - center[1]
                mag = math.sqrt(dXCenter*dXCenter + dYCenter*dYCenter)
                new_distance = radius + BUFFER*2
                newPoint = [center[0] + dXCenter*new_distance/mag, center[1] + dYCenter*new_distance/mag]
                print("Tangent case")
            else:
                point1 = intersection[0]
                point2 = intersection[1]
                lineCenter = [(point1[0]+point2[0])/2,(point1[1]+point2[1])/2]
                dXCenter = lineCenter[0] - center[0]
                dYCenter = lineCenter[1] - center[1]
                dX = point2[0] - point1[0]
                dY = point2[1] - point1[1]
                angle = slopeToAngle(dX,dY)
                angle_check = slopeToAngle(dXCenter,dYCenter)
                choice_1 = angle - math.pi/2
                choice_2 = choice_1 + math.pi
                print("STUFF")
                print(choice_1,choice_2,prev_angle)
                new_angle = choice_1
                if prev_angle:
                    diff1 = min((choice_1-prev_angle)%(math.pi*2),(prev_angle-choice_1)%(math.pi*2))
                    diff2 = min((choice_2-prev_angle)%(math.pi*2),(prev_angle-choice_2)%(math.pi*2))
                    if diff1 > diff2:
                        new_angle = choice_2
                distToCenter = math.sqrt(math.pow(dXCenter,2) + math.pow(dYCenter,2))
                distance = radius + distToCenter
                if math.fabs(new_angle - angle_check) < .01:
                    distance = radius - distToCenter
                    print('hi')
                print(new_angle-angle_check)
                print("ANGLE",new_angle,angle_check)
                new_distance = distance*.5 + radius + BUFFER*2
                print("DISTANCE",distance,new_distance)
                newPoint = [center[0] + new_distance*math.cos(new_angle), center[1] + new_distance*math.sin(new_angle)]

            tempFlight = flight[:count-1]
            temp = [prev,newPoint]
            temp1 = [[x,y]]
            print('Go first:',str(temp),str(temp1),iteration)
            temp = goAround([prev,newPoint],obstacles,iteration+1,prev_angle)
            tempFlight.extend(temp)
            print('Go second')
            temp1 = goAround([newPoint,[x,y]],obstacles,iteration+1,slopeToAngle(newPoint[0]-prev[0],newPoint[1]-prev[1]))[1:]
            print('Done going')
            tempFlight.extend(temp1)
            tempCount = len(tempFlight)
            tempFlight.extend(flight[count+1:])
            print(tempFlight,iteration)

            flight = tempFlight
            count = tempCount - 1
            break

        if count >= len(flight):
            break

        prev = flight[count]
        prev_angle = slopeToAngle(flight[count][0]-flight[count-1][0],flight[count][1]-flight[count-1][1])
        count += 1

    return flight

#waypoints on flight path
currentFlight = [[200, 200], [425, 425], [700,700]]
originalX = [x for [x, y] in currentFlight]
originalY = [y for [x, y] in currentFlight]

#creating obstacles
obstacles = [[[300, 350], 100],[[550,550],80]]
obstacleX = []
obstacleY = []
for center, radius in obstacles:
    oX, oY = createObstacle(center, radius)
    obstacleX.extend(oX)
    obstacleY.extend(oY)

plane = goAround(currentFlight,obstacles,1)
planeX = [x for [x, y] in plane]
planeY = [y for [x, y] in plane]
#goAround(currentFlight,obstacles[0])
#Plotting stuff
plt.plot(originalX, originalY, 'yo')
plt.plot(planeX, planeY, 'ro')
plt.plot(obstacleX, obstacleY, 'bo')
plt.axis([0, 1000, 0, 1000])
plt.show()
