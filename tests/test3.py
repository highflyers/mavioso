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
drone.set_VTOL_mode(mavioso.MAV.VTOL_MODE_PLANE)
Script.Sleep(1000)
try:
    drone.takeoff(50)
except:
    pass
waypoints = []
delta = 0.01
waypoints.append(GeoCoordinate.GeoCoordinate(-37.5858, 143.875, 100))
waypoints.append(GeoCoordinate.GeoCoordinate(-37.5858, 143.875+delta, 100))
waypoints.append(GeoCoordinate.GeoCoordinate(-37.5858-delta, 143.875+delta, 100))
waypoints.append(GeoCoordinate.GeoCoordinate(-37.5858-delta, 143.875, 100))
drone.position_check_threshold = 150
for waypoint in waypoints:
    drone.set_waypoint(waypoint, True)

target = GeoCoordinate.GeoCoordinate(-37.5858-delta/2, 143.875+delta/2, 100)
drone.set_VTOL_mode(mavioso.MAV.VTOL_MODE_QUAD)
drone.set_waypoint(target, True)
