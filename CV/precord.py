from picamera.array import PiRGBArray
from picamera import PiCamera
import sys

from time import sleep

camera = PiCamera()

if len(sys.argv) >3:
	camera.start_preview()
camera.start_recording(sys.argv[1]+'.h264')
sleep(int(sys.argv[2]))
camera.stop_recording()
if len(sys.argv) >3:
	camera.stop_preview()
