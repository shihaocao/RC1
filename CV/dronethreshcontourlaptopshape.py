#9/8/2018 - modulate script to accept video
# import the necessary packages from pyimagesearch.tempimage import asdf
#TempImage
#from 9_8.2dronethreshcontour.py, edited to run on laptop
# from picamera.array import PiRGBArray
# from picamera import PiCamera

#To run: python dronethreshcontourlaptopshape.py C:\Users\zz198\OneDrive\Desktop\RC\testvideos\redtriangle_Trim.mp4
#can add another comment as the threshold
import sys
import argparse
import warnings
import datetime
#import dropbox
import imutils
import json
import time
import cv2
import numpy as np
# import RPi.GPIO as GPIO

vehicle = None

def detectshape(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    # if the shape is a triangle, it will have 3 vertices
    if len(approx) == 3:
        shape = "triangle"

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

    # if the shape is a pentagon, it will have 5 vertices
    elif len(approx) == 5:
        shape = "pentagon"

    # otherwise, we assume the shape is a circle
    else:
        shape = "circle"

    # return the name of the shape
    return shape


def vidprocess():
    global cap, lethalpoints, nonlethal, avg, conf
    global frame, ss, thresh
    global camera, rawCapture, prevtags, usevid
    timestamp = datetime.datetime.now()
    text = "Unoccupied"

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)


    if conf["empty"] == 1:
        blank = np.zeros((500,500,3),np.uint8)
        frame2 = blank
    else:
        frame2 = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 4)
    #gray = frame
    # if the average frame is None, initialize it
    #ret,thresh2 = cv2.threshold(gray,195,255,cv2.THRESH_BINARY)
    gray = cv2.bitwise_not(gray)
    #64 is when we pick up on grass, 20 is when we stop seeing white, 42 is the average, calibrate on test 11
    ret,thresh1 = cv2.threshold(gray,GTHRESH,255,cv2.THRESH_BINARY)
    thresh2 = cv2.bitwise_not(thresh1)
    keypoints = blobber.detect(thresh1)

    cnts = cv2.findContours(thresh2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        #print(cv2.contourArea(c))
        if cv2.contourArea(c) > conf["max_area"]:
            continue
        if cv2.contourArea(c) < conf["min_area"]:
            continue

        print(detectshape(c))
        (x,y,w,h) = cv2.boundingRect(c)

        cv2.rectangle(frame2, (x,y), (x+w, y+h), (0,0,255), 2)

    if len(cnts) > 0:
        print("CONTOUR DETECTED "+str(len(cnts)))
        #opendoor()
    '''for tag in keypoints:
            xc = tag.pt[0]
            yc = tag.pt[1]
            rad = tag.size'''
    #loggedblobs = [database[x][0] for x in database if database[x][1]==0]
    frame2 = cv2.drawKeypoints(frame2, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if not sss:
        cv2.imshow("Security Feed", frame2)
        cv2.imshow("Gray Feed", gray)
        cv2.imshow("Thresh Feed", thresh1)
        #cv2.imshow("Thresh2 Feed", thresh2)
    key = cv2.waitKey(1) & 0xFF
    #cv2.imshow("Frame Delta",frameDelta)
    if key == ord("q"):
        return False
    # clear the stream in preparation for the next frame
    if not usevid:
        rawCapture.truncate(0)
    return True
# def connectvehicle():
#     print(:"Connectin")
#     connection_string = '/dev/ttsS0'
#     arglist = ['paramters' , 'gps_0', 'armed', 'mode','attitude','system_status'. 'location']
#     vehicle = connect(connection_string, wait_ready = True, heartbeat_timeout = 300, baud = 57600)

sss = False
print(sys.argv)
if "sss" in sys.argv:

    sss = True
    print("SSH")

GTHRESH  = 26
for s in sys.argv:
    validnum = True
    try: int (s)
    except ValueError:
        validnum = False
    if validnum:
        GTHRESH=int(s)

usevid = False
print(sys.argv[1])
for s in sys.argv[1:]:
    if '.' in s:
        usevid = True

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--conf", required=True,
#       help="path to the JSON configuration file")
#args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open("conf.json"))
client = None


# initialize the camera and grab a reference to the raw camera capture
# if not usevid:
#     camera = PiCamera()
#     camera.resolution = tuple(conf["resolution"])
#     camera.framerate = conf["fps"]
#     rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

print("video form: " + sys.argv[1])
cap = cv2.VideoCapture(sys.argv[1])
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
#params.minThreshold = 10;
#params.maxThreshold = 200;

# Filter by Area.
params.filterByArea = False
params.minArea = 300

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.0001

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.0001

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Create a detector with the parameters
blobber = cv2.SimpleBlobDetector_create(params)
# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
# servoPIN = 17
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servoPIN, GPIO.OUT)
#
# p = GPIO.PWM(servoPIN, 50)
# p.start(2.5)
# p.ChangeDutyCycle(15)
#     #
#
# #
# def opendoor():
#     p.ChangeDutyCycle(5)
# def arm():


#GTHRESH=26 		#grass threshold, default 26., input string, defualts to 26
# capture frames from the camera
#cap = cv2.VideoCapture(sys.argv[1])

count = 0
if not usevid:
    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # grab the raw NumPy array representing the image and initialize
        # the timestamp and occupied/unoccupied text
        frame = f.array
        vidprocess()
else:
    print("reading from video")
    print("is cap open: "+str(cap.isOpened()))
    while cap.isOpened():
        ret, frame = cap.read()

        if not vidprocess():
            break

cap.release()
cv2.destroyAllWindows()
