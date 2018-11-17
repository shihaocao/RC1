'''Alex Black, camera mapping code'''
import cv2
import numpy as np
import glob
import io
from PIL import Image
from threading import Thread
import collections
import time

##Define camera settings
width = 640
height = 480

#Video Setup
frame = cv2.VideoCapture( 0 )
frame.set( cv2.CAP_PROP_FRAME_WIDTH, width )
frame.set( cv2.CAP_PROP_FRAME_HEIGHT, height )

'''These are specialized settings for individual cameras, uncomment & add lines as nessesary'''
"Logitech c920 series"
ret = 0.30352728557515835
mtx = np.array( [[1.84716013e+03, 0.00000000e+00, 1.07505531e+03], [0.00000000e+00, 1.94353471e+03, 6.43623251e+02], [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]] )
dist = np.array( [[ 0.84586308, -2.9763694, 0.02533502, -0.01567523, 3.79456159]] )
rvecs = np.array( [[-0.29764532], [-0.10690795], [ 0.03223423]] )
tvecs = np.array( [[-15.84659745], [-10.7573455 ], [ 38.38854703]] )
angle = 78
"See3CAM_CU135, standard lens"
#
#angle = 67
"Dell XPS 13 9350 Webcam"
#ret = 0.12383531518402334
#mtx = np.array( [[ 1.02031238e+03, 0.00000000e+00, 6.83758990e+02 ], [ 0.00000000e+00, 1.08132907e+03, 3.80952010e+02 ], [ 0.00000000e+00, 0.00000000e+00, 1.00000000e+00 ]] )
#dist = np.array( [[-0.30859637, 0.47428528, 0.00801277, -0.08025363, -0.74562896]] )
#rvecs = np.array( [[-0.37569308], [-0.43149746], [ 0.5014495 ]] )
#tvecs = np.array( [[-11.74748938], [ -3.30748321], [ 32.67234293]] )
#angle = 66
"GoPro Hero 3+ Black"
#angle = 149.2
"ArduCam 5"
#angle = 68

'''Actual video block'''
i = 0
while True:
    print( i )
    i+=1
    _,pcimg = frame.read()

    ##Black magic here undistorts image
    h,  w = pcimg.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    dst = cv2.undistort( pcimg, mtx, dist, None, newcameramtx )
    x,y,w,h = roi
    ndcimg = dst[y:y+h, x:x+w]
    #Uncomment new two lines to show the pre and post distort images
    cv2.imshow( 'before', pcimg )
    cv2.imshow( 'testout', ndcimg )

    ##All references to the original image after this comment should reference cimg as the undistorted image, and pcimg as the distorted one
    #PUT THY CODE HIER

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
frame.release()
