from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import Counter
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


class BackgroundColorDetector():
    def __init__(self, imageLoc):
        self.img = cv2.imread(imageLoc, 1)
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w*self.h
 
    def count(self):
        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                RGB = (self.img[x,y,2],self.img[x,y,1],self.img[x,y,0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1
 
    def average_colour(self):
        red = 0; green = 0; blue = 0;
        sample = 10
        for top in xrange(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]
 
        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        print "Average RGB for top ten is: (", average_red, ", ", average_green, ", ", average_blue, ")"
 
    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        for rgb, value in self.number_counter:
            print rgb, value, ((float(value)/self.total_pixels)*100)
 
    def detect(self):
        self.twenty_most_common()
        self.percentage_of_first = (float(self.number_counter[0][1])/self.total_pixels)
        print self.percentage_of_first
        if self.percentage_of_first > 0.5:
            print "Background color is ", self.number_counter[0][0]
        else:
            self.average_colour()
 
if __name__ == "__main__":
	print("running")
	
	warnings.filterwarnings("ignore")
	conf = json.load(open("conf.json"))

	camera = PiCamera()
	camera.resolution = tuple(conf["resolution"])
	camera.framerate = conf["fps"]
	rawCapture = PiRGBArray(camera,size=tuple(conf["resolution"]))

	for f in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
		# grab the raw NumPy array representing the image and initialize
    		# the timestamp and occupied/unoccupied text
    		frame = f.array
		text = "Unoccupied"

    		# resize the frame, convert it to grayscale, and blur it
    		frame = imutils.resize(frame, width=500)


        	frame2 = frame
    		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    		gray = cv2.GaussianBlur(gray, (21,21), 4)
		cv2.imwrite("testpic1.png",gray)
		BackgroundColor = BackgroundColorDetector("testpic1.png")
		BackgroundColor.detect()
		break

	
	cv2.destroyAllWindows()
