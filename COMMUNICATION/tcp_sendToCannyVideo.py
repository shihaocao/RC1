import socket
import json
import time
import cv2
import numpy
import imutils

TCP_IP = '127.0.0.1'
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

print("p = pause\nq = quit\nx = end program\ns = save image\ni = send image")
data = input("Please enter command:")
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
        data1 = input("How many frames:")
        frame_num = int(data1)
        data = sock.recv(50)
        sock.send(data1.encode("utf-8"))
        data = sock.recv(50)
        start = time.time()
        for j in range(frame_num):
            print('hi')
            sock.send("READY".encode('utf-8'))
            dimensions_data = sock.recv(100)
            print(dimensions_data)
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
            nparr = numpy.fromstring(image_data, numpy.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            fullimage = imutils.resize(img, width=500)
            end2 = time.time()
            print("Process: ", str(end2-start2))
#            cv2.imwrite('createdFromTCP'+str(j)+'.png',fullimage)
#            image_read = cv2.imread('createdFromTCP'+str(j)+'.png')
            cv2.imshow('createdFromTCP',fullimage)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        end = time.time()
        print('Time Taken: ',str(end-start))
        print("Average Time: ", str((end-start)/frame_num))
    data = input("Please enter command:")
