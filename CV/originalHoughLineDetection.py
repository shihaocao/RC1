import cv2
import numpy as np
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input dataset of images")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
cv2.imshow("Original", img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
cv2.imshow("Edges",edges)
#cv2.waitKey(2000)
#lines = cv2.HoughLines(edges, 1, np.pi / 180, 15, None, 0, 15)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=20,
                    minLineLength=20, maxLineGap=100)
print(len(lines))
previous = []
for x in range(len(lines)):
    for l in lines[x]:
        cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

print(lines)

cv2.imshow('Hough Lines',img)
key = cv2.waitKey(1) & 0xFF
while key != ord("q"):
    key = cv2.waitKey(1) & 0xFF
