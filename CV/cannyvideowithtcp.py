#9/8/2018 - modulate script to accept video
# import the necessary packages from pyimagesearch.tempimage import asdf
#TempImage
#from 9_8.2dronethreshcontour.py, edited to run on laptop
# from picamera.array import PiRGBArray
# from picamera import PiCamera

#To run: python dronethreshcontourlaptopshape2.py C:\Users\zz198\OneDrive\Desktop\RC\testvideos\redtriangle_Trim.mp4
#can add another comment as the threshold
import sys
import argparse
import warnings
import datetime
#import dropbox
import imutils
import threading
import json
import time
import cv2
import numpy as np
import math
import glob
import socket
# import RPi.GPIO as GPIO

vehicle = None

#Global dictionaries
global shapes_dict, boundaries
shapes_dict = {-1: "None", 0: "Circle", 1:"Semi Circle", 2: "Quarter Circle", 3: "Triangle", 4: "Quadliteral", 5: "Pentagon", 6: "Hexagon", 7: "Septagon", 8: "Octagon"}
boundaries = {}
boundaries["RED"] = [[[170,100,200],[200,200,255]]]
boundaries['WHITE'] = [[[220,220,220],[255,255,255]]]


#cv2.waitKey(5000)
def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

def detectshape(frame2, edges):
#    lines = cv2.HoughLines(edges,1,np.pi/180,0)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, None, 20, 25)
    if type(lines) == type(None):
        return -1
    print(len(lines))
    threshDist = 40
    previous = []
#    print(lines)
    for x in range(len(lines)):
        for l in lines[x]:
            noWork = False
            for k in range(x+1, len(lines)):
                j = lines[k][0]
                dist = math.sqrt(math.pow((l[0]-j[0]),2) + math.pow((l[1]-j[1]),2))
                dist1 = math.sqrt(math.pow((l[2]-j[2]),2) + math.pow((l[3]-j[3]),2))
#                print("Distance ", dist+dist1)
                if dist + dist1 < threshDist:
                    noWork = True
            if noWork:
                continue
            previous.append(l)
            cv2.line(frame2, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
#            print('----')
#            print(l[0],l[1])
#            print(l[2],l[3])
    #        print(x2-x1,y2-y1)
    cv2.imshow('Hough Lines',frame2)
    return len(previous)

def vidprocess():
    global cap, lethalpoints, nonlethal, avg, conf
    global frame, ss, thresh, frame2
    global camera, rawCapture, prevtags, usevid
    global drawing, shapes_dict, pause, quit, key_data
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
    auto = auto_canny(thresh2)
#    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    sides = detectshape(frame2, auto)
    print(sides)
    shape = shapes_dict[sides]
    print(shape)
#    cv2.imshow('Thresh2', thresh2)
    keypoints = blobber.detect(thresh1)

    if not sss:
        cv2.imshow("Security Feed", frame2)
        cv2.imshow("Gray Feed", gray)
        cv2.imshow("Thresh Feed", thresh1)
        cv2.imshow("Edges",auto)
#        cv2.waitKey(2000)
        #cv2.imshow("Thresh2 Feed", thresh2)
    key = cv2.waitKey(1) & 0xFF
	#cv2.imshow("Frame Delta",frameDelta)
	#Keys that can be pressed during the video capture
	#key legend, q = quit, d = draw contours, p = pause/unpause
    if key == ord("q"):
        return False
    elif key == ord("d"):
        drawing = not drawing
    elif key == ord("p"):
        pause = not pause

    while pause:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("p"):
            pause = not pause

    if key_data == "QUIT":
        return False
    elif key_data == "SAVEIMG":
        cv2.imwrite("saved_image.png",frame2)

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
if not usevid:
    print("[INFO] warming up...")
    time.sleep(conf["camera_warmup_time"])
else:
    time.sleep(1)
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
stop = False
pause = False
quit = False
key_data = ""

def runvideo():
    global camera, cap, frame, drawing, pause, quit
    if not usevid:
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image and initialize
            # the timestamp and occupied/unoccupied text
            frame = f.array
            vidprocess()
    else:
        print("reading from video")
        print("is cap open: "+str(cap.isOpened()))
        drawing = False
        while cap.isOpened():
            ret, frame = cap.read()

            if not vidprocess():
                break

    cap.release()
    cv2.destroyAllWindows()

def tcp_recieve():
    count = 0
    global pause, key_data, frame2

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM) # TCPaddr
	#sock1 = socket.socket(socket.AF_INET,socket.DGRAM)
    sock.bind((TCP_IP, TCP_PORT))
    print('Binded')
    sock.listen(1)
    print('Listening')
    conn, info = sock.accept()
    print('hi')
    data = 'a'
    while len(data) > 0:
        print('hi')
        data = conn.recv(1024) # buffer size is 1024 bytes
        data = data.decode('utf-8')
        print(data)
        if data == "PAUSE":
            pause = not pause
        elif data == "QUIT":
            key_data = data
        elif data == "EXIT":
            conn.close()
            sock.close()
            break
        elif data == "SAVEIMG":
            key_data = data
        elif data == 'SENDIMG':
            data = conn.recv(1024)
            numofframes = int(data)
            for k in range(numofframes):
                data = conn.recv(1024)
                while data.decode('utf-8') != "READY":
                    key_data = "QUIT"
                    break
#                print('hi')
                sending_frame = imutils.resize(frame2,width=125)
#                print(len(sending_frame),len(sending_frame[0]),len(sending_frame[0][0]))
    			#Sending dimensions of origianl and shrunk image
                dimensions_data = str(len(frame2)) + "," + str(len(frame2[0])) + "," + str(len(sending_frame)) + "," + str(len(sending_frame[0]))
                conn.send(dimensions_data.encode('UTF-8'))
#                print(dimensions_data)
#                key_data = 'QUIT'
                #Sending image data
                fullString = ','.join(str(pixel) for innerlist in sending_frame for item in innerlist for pixel in item)
                fullString = fullString.encode('utf-8')

                conn.sendall(fullString)
                print('FRAME SENT')
                conn.send("DONE".encode('UTF-8'))
#             return False

    key_data = "QUIT"
    conn.close()
    sock.close()
#        sock.sendto(b"Thanks for the input, anything more?",addr)

#Threading
videoThread = threading.Thread(target=runvideo)
videoThread.start()
tcpThread = threading.Thread(target=tcp_recieve)

tcpThread.start()
#cd C:\Users\Srikar\Documents\RC1\CV
#python cannyvideowithtcp.py C:/Users/Srikar/Documents/UAVTestVideos/whitepentagon3.mp4
