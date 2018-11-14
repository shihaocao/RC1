import socket
import json
import time
import cv2
import numpy

UDP_IP = "192.168.1.53"
UDP_PORT = 5005
pause = "PAUSE"
quit = "QUIT"
empty = ""
save_image = "SAVEIMG"
send_image = "SENDIMG"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock.connect((UDP_IP,UDP_PORT))

print("p = pause\nq = quit\nx = end program\ns = save image\ni = send image")
data = input("Please enter command:")
#Commands legend: p = pause, q = quit video, x = end program, s = save image file
while len(data) > 0:
    if data == "p":
        sock.send(pause.encode('utf-8'))
#        sock.sendto(pause.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "q":
        sock.send(quit.encode('utf-8'))
#        sock.sendto(quit.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "x":
        sock.send(empty.encode('utf-8'))
#        sock.sendto(empty.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "s":
        sock.send(save_image.encode('utf-8'))
#        sock.sendto(save_image.encode('utf-8'), (UDP_IP, UDP_PORT))
    elif data == "i":
        sock.send(send_image.encode('utf-8'))
#        buffer = 8192*2
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
#        while image_data != "DONE".encode('utf-8'):
#            compiled += image_data
#            image_data,addr = sock.recv(buffer)
#            print(image_data)
#            print(image_data)
#        done_message = sock.recv(buffer)
#        print(done_message.decode('utf-8'))
        print(width,height)
#        print(compiled)
        image = image_data.decode('utf-8')
#        image = image.replace(' ','')
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
        cv2.imwrite('createdFromSocket.png',fullimage)
#        cv2.imshow('Full Image',fullimage)
#        cv2.waitKey(6000)
#        print(image)
#        print(len(image))
#        print(len(image[0]))
        #image = json.loads(compiled)
        #print(len(image))
        #print(image)
#        image = cv2.imread(image)

#        imagedata_arr = pickle.loads(image_data)
#        cv2.imwrite("Send.png",imagedata_arr)


    data = input("Please enter command:")
