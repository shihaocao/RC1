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
#lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, 0, 15)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 200, threshold = 25, minLineLength = 20, maxLineGap = 1000)

#lines = cv2.HoughLines(edges,1,np.pi/180,15)
print(lines[0])
print(len(lines))
previous = []
#rhoThresh = 50
#thetaThresh = 2*np.pi/9
for x in range(len(lines)):
#    for rho,theta in lines[x]:
    for l in lines[x]:
        noWork = False
#        print(rho,theta)
#        for (prevR,prevT) in previous:
#            if math.fabs(prevT-theta) < thetaThresh or math.fabs(prevT-(np.pi - theta)) < thetaThresh:
#                if math.fabs(prevR-rho) < rhoThresh or math.fabs(prevR-(0-rho)) < rhoThresh:
#                    print('hi')
#                    noWork = True
        if noWork:
            continue
#        previous.append((rho,theta))
        previous.append(l)
#        a = np.cos(theta)
#        b = np.sin(theta)
#        x0 = a*rho
#        y0 = b*rho
#        x1 = int(x0 + 1000*(-b))
#        y1 = int(y0 + 1000*(a))
#        x2 = int(x0 - 1000*(-b))
#        y2 = int(y0 - 1000*(a))

#        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)
#        print(x2-x1,y2-y1)
print(previous)
print(len(previous))
cv2.imshow('Hough Lines',img)
cv2.waitKey(5000)
