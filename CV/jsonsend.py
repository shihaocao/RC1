import socket
import json
from pprint import pprint

UDP_IP = "127.0.0.1"
UDP_PORT = 5005


with open('conf.json') as f:
    data = json.load(f)


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.sendto(json.dumps(data).encode('utf-8'), (UDP_IP, UDP_PORT))
