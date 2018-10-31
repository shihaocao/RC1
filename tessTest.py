#Alex Black
import cv2 
import numpy as np
#import pytesseract as tes
import io
from PIL import Image
from threading import Thread
import collections

i = 0
#
frame = cv2.VideoCapture(0)#v2.imread( 'uncrop.jpg' )
#frame.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
#frame.set(cv2.CAP_PROP_FRAME_HEIGHT,1000)

kern = np.ones( ( 2, 2 ), np.uint8 )
while True:
    i+=1
    print( i )
    #Imput image should be cropped, one image with two colors defining the outline of the target should be inputted, and another one of identical scale with the actual color values
    _,cimg = frame.read()
    #cimg = frame
    #limg = cv2.Laplacian( cimg, cv2.CV_16S, 1000 )
    bwcimg = cv2.cvtColor( cimg, cv2.COLOR_BGR2GRAY )

    #contour = cv2.erode( cv2.imread( 'contour.PNG' ), kern, iterations = 1 )
    #contour = cv2.dilate( cv2.Canny( cv2.blur( cimg, ( 2, 2 ) ), 100, 200 ), kern, iterations = 1 )
    #bwcontour = cv2.cvtColor( contour, cv2.COLOR_BGR2GRAY )

    diff = cv2.cvtColor( cv2.bitwise_xor( cimg, cv2.blur( cimg, ( 2, 2  ) ) ), cv2.COLOR_BGR2GRAY )

    white1 = np.array( [ 10 ] )
    white2 = np.array( [ 256 ] )
    maxdiff = cv2.cvtColor( cv2.inRange( cv2.blur( diff, ( 10, 10 ) ), white1, white2 ), cv2.COLOR_GRAY2BGR )

    

    masked = cv2.bitwise_and( cimg, maxdiff )

    #c1 = np.array( [ 127, 0, 0 ] )
    #c2 = np.array( [ 0, 255, 255 ] )

    #defTargets = cv2.inRange( cimg, c1, c2 )

    edge = cv2.Canny( cv2.blur( cimg, ( 2, 2 ) ), 133, 100 ) 
    
   
    edge = cv2.bitwise_and( edge, cv2.cvtColor( masked, cv2.COLOR_BGR2GRAY ) )

    w1 = np.array( [ 50 ] )
    w2 = np.array( [ 256 ] )
    edge = cv2.cvtColor( cv2.inRange( edge, w1, w2 ), cv2.COLOR_GRAY2BGR )

    dedge = cv2.dilate( edge,  np.ones( ( 5, 5 ), np.uint8 ), iterations = 7 )

    rcimg = cv2.bitwise_and( dedge,  cimg )
    
    cv2.imshow( 'mod', rcimg )
    cv2.imshow( 'ori', cimg )
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
frame.release()
'''
    #All colors done in BGR
    contourIColor = np.array( [ 127, 127, 127 ] )
    contourI2Color = np.array( [ 255, 255, 255 ] )

    #Remove any bit of colorimg where contour has contour-notColor
    masterMask = cv2.inRange( edge, contourIColor, contourI2Color )
    removedBackImg = cv2.bitwise_and( cimg, cimg, mask = masterMask ) 	#Inverts color of target, does not matter in post-processing
    #cv2.imwrite( 'testout.png', removedBackImg )

    #Find average color of target
    averageColor = cv2.mean( removedBackImg, mask = masterMask )

    #Replace any color close to the average color with white
    strength = 50 
    upperBound = np.array( [ averageColor[ 0 ] + strength, averageColor[ 1 ] + strength, averageColor[ 2 ] + strength ] )
    lowerBound = np.array( [ averageColor[ 0 ] - strength, averageColor[ 1 ] - strength, averageColor[ 2 ] - strength ] )

    targetMask = cv2.bitwise_not( cv2.inRange( removedBackImg, lowerBound, upperBound ) )

    whiteTarg = cv2.bitwise_not( cv2.bitwise_and( removedBackImg, removedBackImg, mask = targetMask ) ) 
    #Anything not white or transparent made black
    white = np.array( [ 254, 254, 254 ] )
    morewhite = np.array( [ 256, 256, 256 ] )
    contrast = cv2.inRange( whiteTarg, white, morewhite )

    cv2.imwrite( 'testout.png', contrast ) 
    '''
