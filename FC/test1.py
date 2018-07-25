from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time,sys,argparse,math

print "Connecting"
#connection_string = '127.0.0.1:14540'
connection_string = '/dev/ttyACM0'
vehicle = connect(connection_string, wait_ready = True)

print " Type: %s" % vehicle._vehicle_type
print " Armed: %s" % vehicle.armed
print " System status: %s" % vehicle.system_status.state
print " GPS: %s" % vehicle.gps_0
print " Alt: %s" % vehicle.location.global_relative_frame.alt


