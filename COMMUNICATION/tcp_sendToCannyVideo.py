import socket
import json
import time
import cv2
import numpy
import imutils

TCP_IP = '127.0.0.1'
#TCP_IP = '192.168.1.245'
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

def frame(count):
    sock.send("DIMENSIONS".encode('utf-8'))
#    print("DIMENSIONS")
    dimensions_data = sock.recv(1024)
#    print(dimensions_data)
    sock.send("FRAME".encode('utf-8'))
    [real_width,real_height,width,height] = [int(i) for i in dimensions_data.decode('utf-8').split(',')]
    print(real_width,real_height,width,height)

    buffer = width*height*2 #times two just incase extra data somehow gets sent
#    print(buffer)
    image_data = sock.recv(buffer)
    print(str(count),"GOT IT",str(time.time()))
    print(len(image_data))
    start_process = time.time()
    nparr = numpy.frombuffer(image_data, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    fullimage = img
#    fullimage = imutils.resize(img, width=500)
    end_process = time.time()
    print("Process: ", str(end_process-start_process))
#            cv2.imwrite('createdFromTCP'+str(j)+'.png',fullimage)
#            image_read = cv2.imread('createdFromTCP'+str(j)+'.png')
    cv2.imshow('createdFromTCP',fullimage)
    cv2.waitKey(1)

#Commands legend: p = pause, q = quit video, x = end program, s = save image file
while len(data) > 0:
    if data == "p":
        sock.send(pause.encode('utf-8'))
    elif data == "q":
        sock.send(quit.encode('utf-8'))
    elif data == "x":
        sock.send(exit.encode('utf-8'))
    elif data == "s":
        sock.send(save_image.encode('utf-8'))
    elif data == "i":
        sock.send(send_image.encode('utf-8'))
        seconds = int(input('how many seconds  '))
        print(seconds)
        ready = sock.recv(1024)
        print(ready)
        if ready.decode('utf-8') != "READY":
            print("WRONG")
            print(ready.decode('utf-8'))
            sock.close()
            break
        start = time.time()
        print(start)
        count = 0
        while time.time()-start < seconds:
            frame(count)
            count += 1
        sock.send("ALLDONE".encode('utf-8'))
        print("ALLDONE",str(count))
    data = input("Please enter command:")
    cv2.destroyAllWindows()
