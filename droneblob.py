# import the necessary packages from pyimagesearch.tempimage import 
#TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
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
import RPi.GPIO as GPIO

sss = False
print(sys.argv)
if len(sys.argv) == 2:
	
	sss = True
	print("SSH")

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-c", "--conf", required=True,
#	help="path to the JSON configuration file")
#args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open("conf.json"))
client = None


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
#params.minThreshold = 10;
#params.maxThreshold = 200;

# Filter by Area.
params.filterByArea = True
params.minArea = 150

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.5

# Filter by Inertia
params.filterByInertia = True
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
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)
p.ChangeDutyCycle(15)
#

#
def opendoor():
	p.ChangeDutyCycle(5)

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
	frame = f.array
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
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	#gray = frame
	# if the average frame is None, initialize it
	
	
	keypoints = blobber.detect(gray)
	
	if len(keypoints) > 0:
		print("BLOBS DETECTED "+str(len(keypoints)))
		opendoor()
	'''for tag in keypoints:
		xc = tag.pt[0]
		yc = tag.pt[1]
		rad = tag.size'''
#	loggedblobs = [database[x][0] for x in database if database[x][1]==0]
	frame2 = cv2.drawKeypoints(frame2, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	if not sss:
		cv2.imshow("Security Feed", frame2)
	
	key = cv2.waitKey(1) & 0xFF
	#cv2.imshow("Frame Delta",frameDelta)
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
