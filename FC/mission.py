#from dronekit import connect, Command, LocationGlobal, VehicleMode
import dronekit as dk
import mavutil
import time,sys,argparse,math
import logging

log = logging.getLogger('drone script')
startime = time.time()
log.info ("Connecting")
#connection_string='127.0.0.1:14550'
connection_string = '/dev/ttyS0'
arglist = ['parameters','gps_0','armed','mode','attitude','system_status','location']
vehicle = dk.connect(connection_string, wait_ready = arglist, heartbeat_timeout = 300, baud = 57600)

log.info("Time to connection: %s" % str(time.time()-startime))

cmds = vehicle.commands
#cmds.clear() #clear list of commands to execute
#cmds.upload() #upload list of commands to pixhawk

cmds.download() #get list of commands that vehicle has yet to execute
cmds.wait_ready() #wait untuil downlaod is done
missionlist = [cmds] #put current command list into missionlist
missionlist[0].command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF #chaange first command to takeoff
cmds.clear() #clear vehicles previous list of commands(mission)
for i in missionlist
    cmds.add(i)
cmds.upload()