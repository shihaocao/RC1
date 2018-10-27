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
image2 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,image3 = cv2.threshold(image2,127,255,cv2.THRESH_BINARY_INV)
cnt = cv2.findContours(image3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
#cv2.imwrite(args["image"],image3)
(x,y,w,h) = cv2.boundingRect(cnt)

cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)

cv2.imshow("Image",image)

# create shapedict
shapedict = {"Triangle":"Shapes/TRIANGLE.png",\
				"Square":"Shapes/SQUARE.png",\
				"Trapezoid":"Shapes/TRAPEZOID.PNG",\
				"Quarter Circle":"Shapes/CIRCLE4.PNG",\
				"Pentagon":"Shapes/PENTAGON.PNG"\
			}
for s in shapedict:
	curimage = cv2.imread(shapedict[s])
	curimage2 = cv2.cvtColor(curimage,cv2.COLOR_BGR2GRAY)
	ret,curimage3 = cv2.threshold(curimage2,127,255,cv2.THRESH_BINARY_INV)					#cv detects light contours or dark background


	curcnts = cv2.findContours(curimage3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	(x,y,w,h) = cv2.boundingRect(curcnts[0])

	cv2.rectangle(curimage, (x,y), (x+w, y+h), (0,0,255), 2)

	cv2.imshow(s,curimage)
	shapedict[s] = curcnts[0]


minvalue = 10
minshape = "No Shape"
for s in shapedict:
	curms = cv2.matchShapes(shapedict[s],cnt,1,0.0)
	print(curms)
	if(curms < minvalue):
		minvalue = curms
		minshape = s

#if(minshape!="Triangle"): time.sleep(5)
print(minshape)




cv2.waitKey(20000)
