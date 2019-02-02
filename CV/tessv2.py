'''Alex Black, Code for activly removing most promenent colors in image'''
'''Other notes for experimenting:
    - Consider using cv2.meanStdDev() to find how much the color varies
'''

##Imports
import cv2
import numpy as np
import io
from PIL import Image
from threading import Thread
import collections
import time

##Controlling Variables
numColorRemove = 3
width = 640
height = 480

##Records video
frame = cv2.VideoCapture( 0 )
frame.set( cv2.CAP_PROP_FRAME_WIDTH, width )
frame.set( cv2.CAP_PROP_FRAME_HEIGHT, height )

##Continously processes frames until while True block broken
i = 0
while True:
    ##Counter for frames processed
    i+=1
    print( i )

    ##Read image
    _,cimg = frame.read()

    #cimg = cv2.imread( 'officialY.png' )

    cimg = cv2.GaussianBlur( cimg, ( 3 , 3 ), 0 )

    imgheight, imgwidth, _ = cimg.shape

    ##Applys effects numColorRemove times
    stepmask = cv2.bitwise_not( np.zeros( ( imgheight, imgwidth, 1 ), np.uint8 ) )
    for o in range( 0, numColorRemove ):
        ##replace any color close to the average color with white
        averageColor, strength = cv2.meanStdDev( cimg, mask = stepmask )
        strength ** 2

        upperBound = np.array( [ averageColor[ 0 ] + strength[ 0 ], averageColor[ 1 ] + strength[ 1 ], averageColor[ 2 ] + strength[ 2 ] ] )
        lowerBound = np.array( [ averageColor[ 0 ] - strength[ 0 ], averageColor[ 1 ] - strength[ 1 ], averageColor[ 2 ] - strength[ 2 ] ] )

        stepmask = cv2.bitwise_and( stepmask, stepmask, mask = cv2.bitwise_not( cv2.inRange( cimg, lowerBound, upperBound ) ) )
    step = cv2.bitwise_and( cimg, cimg, mask = stepmask )

    cv2.imshow( 'testout', cimg )
    cv2.imshow( 'edged', step )

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
frame.release()
