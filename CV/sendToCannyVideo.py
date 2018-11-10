import socket
import json
from pprint import pprint
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
pause = "PAUSE"
quit = "QUIT"
empty = ""
save_image = "SAVEIMG"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

data = input("Please enter command:")
#Commands legend: p = pause, q = quit video, x = end program, s = save image file
while len(data) > 0:
    if data == "p":
        sock.sendto(pause.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "q":
        sock.sendto(quit.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "x":
        sock.sendto(empty.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "s":
        sock.sendto(save_image.encode('utf-8'), (UDP_IP, UDP_PORT))
    data = input("Please enter command:")
