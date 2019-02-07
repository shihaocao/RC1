import cv2
import numpy
import base64
import time
import zlib
import hashlib
import Crypto
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
import numpy as np

def eAES(s):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(s)
    return key, ciphertext, tag, cipher
def dAES(key, ciphertext, tag, cipher):
    cipher2 = AES.new(key, AES.MODE_EAX, cipher.nonce)
    return cipher2.decrypt_and_verify(ciphertext, tag)

img = cv2.imread("C:/Users/ganes/Pictures/pol.jpg")
img_str = cv2.imencode(".jpg", img)[1].tostring()
print("Size of image string: " + str(len(img_str)))
img_str = zlib.compress(img_str)
print("Size of compressed string: " + str(len(img_str)))
start = time.time()
akey, aes_str, tag, cipher = eAES(img_str)
end = time.time()
print('Time to encrypt frame: ' + str(1000*(end - start)) + ' ms')

tart = time.time()
aes_str = dAES(akey, aes_str, tag, cipher)
nd = time.time()
x = nd - tart
print('Time to decrypt frame: ' + str(1000*x) + ' ms')

aes_str = zlib.decompress(aes_str)
nparr = numpy.frombuffer(aes_str, numpy.uint8)
fullimage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow("AES decoded", fullimage)
cv2.waitKey(3000)
