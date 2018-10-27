#10/27/18, shape detection using image moments/hu moments/matchshapes
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

TRIANGLE = cv2.imread("Shapes/TRIANGLE.png")
SQUARE = cv2.imread("Shapes/SQUARE.png")
SQUARE = cv2.bitwise_not(SQUARE)
image = cv2.bitwise_not(image)

TRIANGLE = cv2.cvtColor(TRIANGLE, cv2.COLOR_BGR2GRAY)
SQUARE = cv2.cvtColor(SQUARE, cv2.COLOR_BGR2GRAY)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

TRIANGLECNTS= cv2.findContours(TRIANGLE,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
SQUARECNTS = cv2.findContours(SQUARE,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
imagecnts = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]



print("With Triangle:",cv2.matchShapes(TRIANGLECNTS,imagecnts,1,0.0))
print("With Square:",cv2.matchShapes(SQUARECNTS,imagecnts,1,0.0))


cv2.imshow("Triangle",TRIANGLE)
cv2.imshow("Square",SQUARE)
cv2.imshow("Image",image)

cv2.waitKey(20000)
