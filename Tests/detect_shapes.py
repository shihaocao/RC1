from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
from shapedetector import ShapeDetector
import argparse
import imutils
import time
import cv2
 
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-0,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=24,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="H264",
	help="codec of output video")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
 
# initialize the FourCC, video writer, dimensions of the frame, and
# zeros array
fourcc = cv2.VideoWriter_fourcc(*args["codec"])
writer = None
(h, w) = (None, None)
zeros = None



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
 
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
 
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)
 
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)
 
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)

while True:
	# grab the frame from the video stream and resize it to have a
	# maximum width of 300 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=1920)
 
	# check if the writer is None
	if writer is None:
		# store the image dimensions, initialzie the video writer,
		# and construct the zeros array
		(h, w) = frame.shape[:2]
		writer = cv2.VideoWriter(args["output"], fourcc, args[""],
			(w * 2, h * 2), True)
		zeros = np.zeros((h, w), dtype="uint8")
# break the image into its RGB components, then construct the
	# RGB representation of each frame individually
	(B, G, R) = cv2.split(frame)
	R = cv2.merge([zeros, zeros, R])
	G = cv2.merge([zeros, G, zeros])
	B = cv2.merge([B, zeros, zeros])
 
	# construct the final output frame, storing the original frame
	# at the top-left, the red channel in the top-right, the green
	# channel in the bottom-right, and the blue channel in the
	# bottom-left
	output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
	output[0:h, 0:w] = frame
	output[0:h, w:w * 2] = R
	output[h:h * 2, w:w * 2] = G
	output[h:h * 2, 0:w] = B
 
	# write the output frame to file
	writer.write(output)
	# show the frames
	cv2.imshow("Frame", frame)
	cv2.imshow("Output", output)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
print("[INFO] cleaning up...")
#cv2.destroyAllWindows()
vs.stop()
writer.release()
