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
        data1 = input("How many frames:")
        frame_num = int(data1)
        sock.send(send_image.encode('utf-8'))
        sock.send(data1.encode("utf-8"))
        start = time.time()
        print('hi')
        for j in range(frame_num):
            print('hi')
            sock.send("READY".encode('utf-8'))
            dimensions_data = sock.recv(1024)
            [real_width,real_height,width,height] = [int(i) for i in dimensions_data.decode('utf-8').split(',')]
#            print(real_width,real_height,width,height)

            buffer = 5000000
            image_data = sock.recv(buffer)
            print(len(image_data))
            done_statement = sock.recv(1024)
#            print(width,height)
            image = image_data.decode('utf-8')
            image = image[0:len(image)-1]
#            print(len(image))
            image1 = image.split(',')
#            print(len(image1))
            fullimage = []
            row = []
            for i in range(int(len(image1)/3)):
                pixel = image1[i*3:i*3+3]
                pixel = [int(j) for j in pixel]
                pixel = numpy.array(pixel, dtype = "uint8")
                row.append(pixel)
                if len(row) >= height:
                    fullimage.append(numpy.array(row))
                    row = []
            fullimage = numpy.array(fullimage)
            print(len(fullimage))
            print(len(fullimage[0]))
            print(type(fullimage[0][0][0]))
            fullimage = imutils.resize(fullimage, width=500)
#            cv2.imwrite('createdFromTCP'+str(j)+'.png',fullimage)
#            image_read = cv2.imread('createdFromTCP'+str(j)+'.png')
            cv2.imshow('createdFromTCP',fullimage)
            cv2.waitKey(5)
#            cv2.imshow('Image',fullimage)
#            cv2.waitKey(10)
        cv2.destroyAllWindows()
        end = time.time()
        print('Time Taken: ',str(end-start))
        print("Average Time: ", str((end-start)/frame_num))
    data = input("Please enter command:")
