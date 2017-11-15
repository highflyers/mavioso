import sys
import clr
import MissionPlanner
clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t
from MAVLink import MAV_CMD
import MAVLink
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp

print(__file__)
import os

os.path.realpath(__file__)

def doVtolTransition():
	status = MAV.doCommand(MAVLink.MAV_CMD.DO_VTOL_TRANSITION, 0,0, 500, float('nan'), cs.lat, cs.lng, 0)
	print("doVtolTransition {0}".format(status))
	
def takeoff(alt):
	status = MAV.doCommand(MAVLink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, float(alt));
	print("takeoff {0}".format(status))
	
def arm():
	status = MAV.doARM(True)
	print("ARM {0}".format(status))
	
alt = 15.0
home_lat = cs.lat
home_lng = cs.lng
idmavcmd = MAVLink.MAV_CMD.WAYPOINT
id = int(idmavcmd)
Script.ChangeMode("GUIDED")
arm();
Script.Sleep(1000)
takeoff(alt)
while(cs.alt < 0.5*alt):
	Script.Sleep(100);
	print(cs.alt)
	
wp1 = Locationwp().Set(home_lat + 1,home_lng,50, id)
MAV.setGuidedModeWP(wp1, True)
Script.Sleep(10*1000);
wp1 = Locationwp().Set(home_lat + 1,home_lng+1,50, id)
MAV.setGuidedModeWP(wp1, True)
Script.Sleep(10*1000);
wp1 = Locationwp().Set(home_lat - 1,home_lng+1,50, id)
MAV.setGuidedModeWP(wp1, True)
Script.Sleep(10*1000);
wp1 = Locationwp().Set(home_lat,home_lng,50, id)
MAV.setGuidedModeWP(wp1, True)
Script.Sleep(40*1000);
Script.ChangeMode("QLAND")
	

