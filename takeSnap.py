
# Made By Jacob Consalvi, and uploaded at 1/20/18 for the TJHSST First Robotics Team
#Power Cube recognition and tracking
'''When the button a is pressed, the program goutputs the distance to the power cube in feet, the angle from the normal to the robot in radians,
 and the  distance from center  in inches as an array.'''

#from networktables import NetworkTables as NT
#robotIP = 10.34.55.2
import sys
#import serial
PY3 = sys.version_info[0] == 3
import numpy as np
import cv2 as cv
import math
'''ser = serial.Serial()
ser.port = 'USB\VID_3923&PID_762F\\03060EF6'

ser.baudrate = 9600
ser.timeout = 0
ser.open()''' #This is the code sor the rs-232 serial conection



if PY3:
    xrange = range




def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv.GaussianBlur(img, (9,9), 0)
    #img = cv.medianBlur(img,7)
    squares = []
    for gray in cv.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares


cap = cv.VideoCapture(1)
#cap = cv.VideoCapture('testvideo2.mp4')
'''try:
    while(1):
        _,frame = cap.read()

        imgOR = frame
        imgOR = cv.resize(imgOR, (640,480))

        hsv = cv.cvtColor(imgOR, cv.COLOR_BGR2HSV)
        centerx = 0

        lower_Yellow = np.array([5,110,120])
        upper_Yellow = np.array([90,255,255])

        mask = cv.inRange(imgOR, lower_Yellow, upper_Yellow)
        res = cv.bitwise_and(imgOR,imgOR, mask= mask)

        squares = find_squares(res)
        theta = 0
        DistanceFEET = 0
        distanceFromCenterINCH = 0
        if squares != []:
            centerx = round((squares[0][0][0] + squares[0][3][0] + squares[0][1][0]+squares[0][2][0])/4)
            centery = round((squares[0][0][1] + squares[0][3][1] + squares[0][1][1]+squares[0][2][1])/4)

            BottomSideLength = abs(round(squares[0][0][0]) - round(squares[0][2][0]))
            DistanceINCH = 8028/BottomSideLength
            DistanceFEET = DistanceINCH/12

            center = [int(centerx),int(centery)]

            distanceFromCenterPixels = (centerx-320)
            pixelDistanceINCH = 13/BottomSideLength
            pixelDistanceFEET = pixelDistanceINCH/12
            distanceFromCenterINCH = pixelDistanceINCH*distanceFromCenterPixels
            distanceFromCenterINCHoffset = distanceFromCenterINCH - 2.5
            distanceFromCenterFEET = distanceFromCenterINCH/12
            theta = math.asin(distanceFromCenterINCH/DistanceINCH)

            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(imgOR,'CENTER',(center[0],center[1]),font,2,(0,255,0),1,cv.LINE_AA)
            cv.circle(imgOR,(center[0],center[1]),3,(0,255,0),-1)
            cv.circle(imgOR,(320,240),5,(255,255,255),-1)



            #print('Distance Away in feet: ', DistanceFEET, 'horizontal distance from center in inchs: ', distanceFromCenterINCH, 'Angle: ', theta)
            #print(pixelDistanceINCH)
            if cv.waitKey(33) == ord('a'):
                print(DistanceFEET,theta,distanceFromCenterINCH)
                print(ser.name)
                ser.write('Test')
        bytesRead = len(ser.read(10))
        if bytesRead >0 :
            IN = ser.read(bytesRead)
            print(IN)

        cv.drawContours( imgOR, squares, -1, (0, 255, 0), 3 )
        #if squares != []:
            #cv.circle(imgOR,(squares[0][0][0],squares[0][0][1]),5,(225,0,0),-1)
            #cv.circle(imgOR,(squares[0][3][0],squares[0][3][1]),5,(225,0,0),-1)

        cv.imshow('squares', imgOR)
        cv.imshow('Mask', res)




        k = cv.waitKey(5)
        if k == 27:
            break


    #cv.destroyAllWindows()
    #cap.release()

except:
    print('')
    pass'''
#NT.initialize(server = '10.34.55.2')
alexframe = 0;
while(1):
    alexframe = alexframe + 1;
    print(alexframe)
    _, frame = cap.read()

    imgOR = frame
    imgOR = cv.resize(imgOR, (640,480))

    #hsv = cv.cvtColor(imgOR, cv.COLOR_BGR2HSV)
    centerx = 0

    lower_Yellow = np.array([0, 0, 0])
    upper_Yellow = np.array([255, 10, 10])

    mask = cv.inRange(imgOR, lower_Yellow, upper_Yellow)
    res = cv.bitwise_and(imgOR,imgOR, mask= mask)

    squares = find_squares(res)
    theta = 0
    DistanceFEET = 0
    distanceFromCenterINCH = 0
    if squares != []:
        centerx = round((squares[0][0][0] + squares[0][3][0] + squares[0][1][0]+squares[0][2][0])/4)
        centery = round((squares[0][0][1] + squares[0][3][1] + squares[0][1][1]+squares[0][2][1])/4)

        BottomSideLength = abs(round(squares[0][0][0]) - round(squares[0][2][0]))
        DistanceINCH = 8028/BottomSideLength
        DistanceFEET = DistanceINCH/12

        center = [int(centerx),int(centery)]

        distanceFromCenterPixels = (centerx-320)
        pixelDistanceINCH = 13/BottomSideLength
        pixelDistanceFEET = pixelDistanceINCH/12
        distanceFromCenterINCH = pixelDistanceINCH*distanceFromCenterPixels
        distanceFromCenterINCHoffset = distanceFromCenterINCH - 2.5
        distanceFromCenterFEET = distanceFromCenterINCH/12
        theta = math.asin(distanceFromCenterINCH/DistanceINCH)

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(imgOR,'CENTER',(center[0],center[1]),font,2,(0,255,0),1,cv.LINE_AA)
        cv.circle(imgOR,(center[0],center[1]),3,(0,255,0),-1)
        cv.circle(imgOR,(320,240),5,(255,255,255),-1)



        #print('Distance Away in feet: ', DistanceFEET, 'horizontal distance from center in inchs: ', distanceFromCenterINCH, 'Angle: ', theta)
        #print(pixelDistanceINCH)
        if cv.waitKey(33) == ord('a'):
            table = NT.getTable("PIcamera")
            print(DistanceFEET,theta,distanceFromCenterINCH)
            table.putNumber('d1', DistanceFEET)
            table.putNumber('theta', theta)
            table.putNumber('d2', distanceFromCenterINCH)
           # print("thing")
            #ser.write('Test')
            #ser.write(DistanceFEET,theta,distanceFromCenterINCH)

    #bytesRead = len(ser.read(10))
   # if bytesRead >0 :
       # IN = ser.read(bytesRead)
       # print(IN)

    cv.drawContours( imgOR, squares, -1, (0, 255, 0), 3 )
    #if squares != []:
        #cv.circle(imgOR,(squares[0][0][0],squares[0][0][1]),5,(225,0,0),-1)
        #cv.circle(imgOR,(squares[0][3][0],squares[0][3][1]),5,(225,0,0),-1)

    cv.imshow('squares', imgOR)
    cv.imshow('Mask', res)




    k = cv.waitKey(5)
    if k == 27:
        break


cv.destroyAllWindows()
cap.release()
