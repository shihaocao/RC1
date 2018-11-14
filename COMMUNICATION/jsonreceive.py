import socket
from pprint import pprint
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

data = ''
while len(data)<10:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    d = json.loads(data.decode('utf-8'))
print("WRITING TO TEST.JSON")

printStr = json.dumps(d)

with open("test.json","w") as f:
    f.write(printStr)



################################
