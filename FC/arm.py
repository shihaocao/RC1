#arm
from dronekit import connect, Command, LocationGlobal
#from pymavlink import mavutil
import time,sys,argparse,math

startime = time.time()
print ("Connecting")
#connection_string = '127.0.0.1:14540'
connection_string = '/dev/ttyACM0'
arglist = ['parameters','gps_0','armed','mode','attitude','system_status','location']
vehicle = connect(connection_string, wait_ready = False, heartbeat_timeout = 300)

print("Time to connection: %s" % str(time.time()-startime))
print(" Type: %s" % vehicle._vehicle_type)
print(" Armed: %s" % vehicle.armed)
print(" System status: %s" % vehicle.system_status.state)
print(" GPS: %s" % vehicle.gps_0)
print(" Alt: %s" % vehicle.location.global_relative_frame.alt)
print("GPS coordinates %s" % vehicle.location.global_frame)
print("Armed: %s" % vehicle.armed)

print("isarmable: %s" % vehicle.is_armable)

vehicle.armed=True
print("Armed after: %s" % vehicle.armed)
