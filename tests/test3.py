import sys
sys.path.append(r"C:\maciej\projects\mavioso")

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
import mavioso.GeoCoordinate as GeoCoordinate
import mavioso.logging as logging

logging.info("started")

Script.ChangeMode("GUIDED")

drone = mavioso.MAV.MAV(Script, MAV, MAVLink, cs)
drone.arm()
Script.Sleep(1000)
drone.takeoff(50)
for i in range(1):
    print(i)
    Script.Sleep(1000)
drone.set_waypoint(GeoCoordinate.GeoCoordinate(0.1, 0.1, 100))
