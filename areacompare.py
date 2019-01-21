#Alex Black
import cv2
import numpy as np
import io
from PIL import Image
from threading import Thread
import collections

frame = cv2.VideoCapture( 1 )
kern = np.ones( ( 1, 1 ), np.uint8 )

i = 0
while True:
    i+=1
    #print( i )
    _,cimg = frame.read()

    cimg = cv2.imread( 'test.png' )

    cimgh, cimgw, _ = cimg.shape

    cimg = cv2.blur( cimg, ( 1, 1 ) )   #Quick blur removes some of the worst artifacts

    bwcimg = cv2.cvtColor( cimg, cv2.COLOR_BGR2GRAY )
    '''This section isolates areas'''
    diff = cv2.cvtColor( cv2.bitwise_xor( cimg, cv2.blur( cimg, ( 5, 5 ) ) ), cv2.COLOR_BGR2GRAY )
    white1 = np.array( [ 10 ] )
    white2 = np.array( [ 256 ] )
    maxdiff = cv2.cvtColor( cv2.inRange( cv2.blur( diff, ( 5, 5 ) ), white1, white2 ), cv2.COLOR_GRAY2BGR )
    edge = cv2.bitwise_and( cv2.Canny( cv2.blur( cimg, ( 2, 2 ) ), 133, 100 ), cv2.cvtColor( cv2.bitwise_and( cimg, maxdiff ), cv2.COLOR_BGR2GRAY ) )
    w1 = np.array( [ 50 ] )
    w2 = np.array( [ 256 ] )
    edge = cv2.cvtColor( cv2.inRange( edge, w1, w2 ), cv2.COLOR_GRAY2BGR )
    dedge = cv2.dilate( edge, np.ones( ( 5, 5 ), np.uint8 ), iterations = 3 )
    rcimg = cv2.bitwise_and( dedge,  cimg )

    '''This section is for contour identification'''
    bwcimg = cv2.cvtColor( rcimg, cv2.COLOR_BGR2GRAY )
    ret, thresh = cv2.threshold( bwcimg, 0, 255, 0 )
    dthresh = cv2.dilate( thresh, np.ones( ( 5, 5 ), np.uint8 ), iterations = 5 )
    im2, contours, hierarchy = cv2.findContours( thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
    #cv2.drawContours( cimg, contours, -1, ( 0, 255, 0 ), 3 )

    fMask = np.zeros( ( cimgh, cimgw ), np.uint8 )
    cMask = np.zeros( ( cimgh, cimgw ), np.uint8 )
    for o in contours:
        cv2.fillPoly( cMask, pts = [ o ], color = 255 )
        pcontavg = cv2.meanStdDev( bwcimg, mask = cMask )
        pcontmodavg = cv2.meanStdDev( bwcimg, mask = cv2.dilate( cMask, np.ones( ( 5, 5 ), np.uint8 ), iterations = 1 ) )
        print( pcontavg[ 1 ][ 0 ], pcontmodavg[ 1 ][ 0 ] )
        if(  abs( pcontavg[ 1 ][ 0 ] - pcontmodavg[ 1 ][ 0 ] ) < 25 and abs( pcontavg[ 1 ][ 0 ] - pcontmodavg[ 1 ][ 0 ] ) > 15 ):
            fMask = cv2.bitwise_or( fMask, cMask )
        cMask = np.zeros( ( cimgh, cimgw ), np.uint8 )

    '''Just some other things, display mostly'''
    cv2.imshow( 'ori', cimg )
    cv2.imshow( 'cut1', cv2.bitwise_and( cv2.cvtColor( dthresh, cv2.COLOR_GRAY2BGR ), cimg ) )
    cv2.imshow( 'cut2', cv2.bitwise_and( cv2.cvtColor( fMask, cv2.COLOR_GRAY2BGR ), cimg ) )

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
frame.release()
