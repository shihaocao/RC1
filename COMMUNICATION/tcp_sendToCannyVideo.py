import socket
import json
import time
import cv2
import numpy
import imutils

TCP_IP = '192.168.1.245'
TCP_PORT = 5005
pause = "PAUSE"
quit = "QUIT"
exit = "EXIT"
save_image = "SAVEIMG"
send_image = "SENDIMG"
count = 0
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
sock.connect((TCP_IP, TCP_PORT))

print("p = pause\nq = quit\nx = end program\ns = save image\ni = send image\nt = stream")
data = input("Please enter command:")

def frame():
    sock.send("DIMENSIONS")
    start = time.time()

    dimensions_data = sock.recv(100)
    print(dimensions_data)
    sock.send("FRAME".encode('utf-8'))
    [real_width,real_height,width,height] = [int(i) for i in dimensions_data.decode('utf-8').split(',')]
    print(real_width,real_height,width,height)

    buffer = width*height*10 + 10 #10000 just incase extra data somehow gets sent
    print(buffer)
    start1 = time.time()
    image_data = sock.recv(buffer)
    print(time.time())
    end1 = time.time()
    print("Receiving time: ", str(end1-start1))
    print(len(image_data))
    start2 = time.time()
    fullimage = []
    row = []
    nparr = numpy.frombuffer(image_data, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    fullimage = imutils.resize(img, width=500)
    end2 = time.time()
    print("Process: ", str(end2-start2))
#            cv2.imwrite('createdFromTCP'+str(j)+'.png',fullimage)
#            image_read = cv2.imread('createdFromTCP'+str(j)+'.png')
    cv2.imshow('createdFromTCP',fullimage)
    cv2.waitKey(1)

#Commands legend: p = pause, q = quit video, x = end program, s = save image file
while len(data) > 0:
    if data == "p":
        sock.send(pause.encode('utf-8'))
    elif data == 't':
        sock.send('STREAM'.encode('utf-8'))
    elif data == "q":
        sock.send(quit.encode('utf-8'))
    elif data == "x":
        sock.send(exit.encode('utf-8'))
    elif data == "s":
        sock.send(save_image.encode('utf-8'))
    elif data == "i":
        seconds = int(input('how many seconds  '))
        start = time.time()
        while time.time()-start < seconds:
            frame()
        sock.sendAll("ALLDONE")
    data = input("Please enter command:")
    cv2.destroyAllWindows()
