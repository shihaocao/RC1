from dronekit import connect, Command, LocationGlobal, VehicleMode
import dronekit as dk
from pymavlink import mavutil
import time,sys,argparse,math
import logging
import dronekit_sitl
import dronekit

# heavyily influenced by https://github.com/dronekit/dronekit-python/blob/master/examples/mission_import_export/mission_import_export.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('drone script')
parser = argparse.ArgumentParser(description='Demonstrates mission import/export from a file.')
parser.add_argument('-s', action='store_true',
                   help="Flag to start simulated vehicle")
args = parser.parse_args()

sitl=None
def initvehicle():
    if args.s:
        #sitl = dronekit_sitl.start_default()
        sitl = dronekit_sitl.SITL() # load a binary path (optional)
        sitl.download("plane", "3.3.0", verbose=True)
        launchargs = []
        sitl.launch(launchargs, verbose=True, await_ready=True, restart=True)
        #sitl.block_until_ready(verbose=True) # explicitly wait until receiving commands
        connection_string = sitl.connection_string()
        #print("connect to: "+connection_string)
        #connection_string='tcp:127.0.0.1:5760'
    else:
        connection_string = '/dev/ttyS0'
    arglist = ['parameters','gps_0','armed','mode','attitude','system_status','location']
    startime = time.time()
    log.info ("Connecting")
    vehicle= dk.connect(connection_string, wait_ready = arglist, heartbeat_timeout = 300)#, baud = 57600)
    log.info("Time to connection: %s" % str(time.time()-startime))
    while not vehicle.is_armable:
        log.info(" Waiting for vehicle to initialise...")
        time.sleep(1)
    return vehicle

vehicle = initvehicle()

def readmission(aFileName):
    """
    Load a mission from a file into a list. The mission definition is in the Waypoint file
    format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).
    This function is used by upload_mission().
    """
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split('\t')
                ln_index=int(linearray[0])
                ln_currentwp=int(linearray[1])
                ln_frame=int(linearray[2])
                ln_command=int(linearray[3])
                ln_param1=float(linearray[4])
                ln_param2=float(linearray[5])
                ln_param3=float(linearray[6])
                ln_param4=float(linearray[7])
                ln_param5=float(linearray[8])
                ln_param6=float(linearray[9])
                ln_param7=float(linearray[10])
                ln_autocontinue=int(linearray[11].strip())
                cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                missionlist.append(cmd)
    return missionlist

def testinguploaddownload(aFileName):
    missionlist = readmission(aFileName)
    print("\nUpload mission from a file: %s" % aFileName)
    #Clear existing mission from vehicle
    print(' Clear mission')
    cmds = vehicle.commands
    cmds.clear()
    #Add new mission to vehicle
    for command in missionlist:
        print(command)
        cmds.add(command)

    print(' Upload mission')
    time.sleep(3)
    vehicle.commands.upload()

    """
    Downloads the current mission and returns it in a list.
    It is used in save_mission() to get the file information to save.
    """
    print(" Download mission from vehicle")
    missionlist=[]
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
        print(cmd)
    return missionlist

testinguploaddownload("mission2.waypoints")
'''
print("Got vehicle")

cmds = vehicle.commands
print('got commands')
cmds.clear()
print('cleared commands')
lat = -34.364114,
lon = 149.166022
altitude = 30.0
cmd = Command(0,0,0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0, 0, 0, 0, 0, 0,
    lat, lon, altitude)
cmds.add(cmd)
print('added command')
vehicle.commands.upload()
print('uploaded commands')
time.sleep(3);
cmds = vehicle.commands
print('got commands')
cmds.download()
print('downloaded commands')
cmds.wait_ready()
print('waiting commands')

for cmd in cmds:
    print(cmd)
'''
