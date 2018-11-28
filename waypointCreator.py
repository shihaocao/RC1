from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil

def get_location_metres(original_location, dNorth, dEast):
    """
    Finds new location with n degrees north and e degrees east of current location
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)


def addWaypoint(aLocation,dNorth,dEast): #Adds waypoint 
    """
    Adds a takeoff command and one waypoint command to the current mission. 
    Waypoint location is dNorth meters to the north and dEast meters to the east of the specified location
    
    The function assumes vehicle.commands matches the vehicle mission state 
    (you must have called download at least once in the session and after clearing the mission)
    """	

    cmds = vehicle.commands

    print("Clear any existing commands")
    cmds.clear() 
    
    print(" Define/add new commands.")
    # Add new commands. The meaning/order of the parameters is documented in the Command class. 
     
    #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

    #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
    point1 = get_location_metres(aLocation, dNorth, dEast)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
    #add dummy waypoint "2" at point 1 (lets us know when have reached destination)
    #cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 14))    

    print(" Upload new commands to vehicle")
    cmds.upload()

def download_mission():
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready() # wait until download is complete.
    
addWaypoint(vehicle.location.global_frame,50,25)    
download_mission()
