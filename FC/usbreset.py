from usb.core import find as finddev
dev = finddev(idVendor=0x26ac,idProduct=0x0011)
dev.reset()

