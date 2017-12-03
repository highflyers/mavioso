import sys
# sys.path.append(r"C:\Python27amd64\Lib")
sys.path.append(r"C:\Users\wojci\OneDrive\Studia\HF\MAVIOSO\mavioso")

import clr
import MissionPlanner
clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t
from MAVLink import MAV_CMD
clr.AddReference("MissionPlanner.Utilities")
from MissionPlanner.Utilities import Locationwp

import mavioso.MAV

print('start script')
drone = mavioso.MAV.MAV(Script, MAV, MAVLink, cs)
drone.q_loiter()
Script.Sleep(1000)
