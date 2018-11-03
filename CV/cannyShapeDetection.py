import numpy as np
import argparse
import cv2
import imutils
import glob
# construct the argument parse and parse the arguments

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input dataset of images")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
# load the image, convert it to grayscale, and blur it slightly
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
# apply Canny edge detection using a wide threshold, tight
# threshold, and automatically determined threshold
wide = cv2.Canny(blurred, 10, 200)
tight = cv2.Canny(blurred, 225, 250)
auto = auto_canny(blurred)
# show the images
cv2.imshow("Original", image)
#cv2.imshow("Wide", wide)
#cv2.imshow("Tight", tight)
cv2.imshow("Auto", auto)
print(auto)
print(len(auto))
print(len(auto[0]))
print(len(image))
print(len(image[0]))
#print(auto[197][243])
#cv2.imshow("Edges", np.hstack([wide, tight, auto]))
cv2.waitKey(5000)
