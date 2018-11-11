import socket
import json
import time
import cv2
import numpy
print('hi')
'''
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
pause = "PAUSE"
quit = "QUIT"
empty = ""
save_image = "SAVEIMG"
send_image = "SENDIMG"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
sock.connect((TCP_IP, TCP_PORT))

print("p = pause\nq = quit\nx = end program\ns = save image\ni = send image")
data = input("Please enter command:")
#Commands legend: p = pause, q = quit video, x = end program, s = save image file
while len(data) > 0:
    if data == "p":
        sock.send(pause.encode('utf-8'))
    elif data == "q":
        sock.send(quit.encode('utf-8'))
    elif data == "x":
        sock.send(empty.encode('utf-8'))
    elif data == "s":
        sock.send(save_image.encode('utf-8'))
    elif data == "i":
        sock.send(send_image.encode('utf-8'))
        print('hi')
        buffer = 4096
        sock.send(str(buffer).encode('utf-8'))
        print('buffer sent')
        width_data = sock.recv(buffer)
        print(width_data)
        width = int(width_data.decode('utf-8'))
        time.sleep(0.5)
        height_data = sock.recv(buffer)
        height = int(height_data.decode('utf-8'))

        compiled = b""
        buffer = 8192000
        image_data = sock.recv(buffer)
        print(width,height)
        image = image_data.decode('utf-8')
        image = image[0:len(image)-1]
        print(len(image))
        image1 = image.split(',')
        print(len(image1))
        fullimage = []
        row = []
        for i in range(int(len(image1)/3)):
            pixel = image1[i*3:i*3+3]
            pixel = [int(j) for j in pixel]
            pixel = numpy.array(pixel)
            row.append(pixel)
            if len(row) >= height:
                fullimage.append(numpy.array(row))
                row = []
        fullimage = numpy.array(fullimage)
        print(len(fullimage))
        print(len(fullimage[0]))
        cv2.imwrite('createdFromTCP.png',fullimage)

    data = input("Please enter command:")
'''

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
print('hi')
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

print('hi')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('hi')
s.connect((TCP_IP, TCP_PORT))
print('hi')
s.send(MESSAGE)
print('hi')
data = s.recv(BUFFER_SIZE)
print('hi')
s.close()
print('hi')

print("received data:", data)
