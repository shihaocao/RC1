#dronekit-sitl plane

#from dronekit import connect, Command, LocationGlobal, VehicleMode
import dronekit as dk
from pymavlink import mavutil
import time,sys,argparse,math
import logging
import dronekit_sitl
import dronekit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('drone script')


parser = argparse.ArgumentParser(description='Demonstrates mission import/export from a file.')
parser.add_argument('-s', action='store_true',
                   help="Flag to start simulated vehicle")
args = parser.parse_args()

if args.s:
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    #connection_string='tcp:127.0.0.1:5760'
else:
    sitl = None
    connection_string = '/dev/ttyS0'

startime = time.time()
log.info ("Connecting")

arglist = ['parameters','gps_0','armed','mode','attitude','system_status','location']
vehicle= dk.connect(connection_string, wait_ready = arglist, heartbeat_timeout = 300, baud = 57600)
log.info("Time to connection: %s" % str(time.time()-startime))

cmds = vehicle.commands
cmds.clear() #clear list of commands to execute
cmds.upload() #upload list of commands to pixhawk

cmds.download() #get list of commands that vehicle has yet to execute
cmds.wait_ready() #wait untuil downlaod is done
#print(cmds)
missionlist = [cmds] #put current command list into missionlist
print(missionlist)
#missionlist[0].command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF #chaange first command to takeoff

#cmds.clear() #clear vehicles previous list of commands(mission)
#for i in missionlist:
#    cmds.add(i)
#cmds.upload()
print('done')
time.sleep(1000000000)
