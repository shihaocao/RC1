import cv2
import numpy
from Crypto.Cipher import AES
img = cv2.imread("C:/Users/Srikar/Documents/RC1/CV/createdFromSocket.PNG")
img_str = cv2.imencode('.jpg', img)[1].toString()
print(len(img_str))



image_data = img_str
print(len(image_data))
nparr = numpy.frombuffer(image_data, numpy.uint8)
fullimage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("Decoded", fullimage)
