import sys

sys.path.append(r"C:\Python27amd64\Lib")
sys.path.append(r"F:\Australia\mavioso\mavioso")

import sys
import clr
import threading
import Queue
import time
import MissionPlanner

clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t
from MAVLink import MAV_CMD
import MAVLink

clr.AddReference("MissionPlanner.Utilities")  # includes the Utilities class
from MissionPlanner.Utilities import Locationwp

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import mavioso.MAV
import mavioso.MAV_controller
import mavioso.PathTracker
import mavioso.GeoCoordinate as GeoCoordinate
import mavioso.http_server
import mavioso.logging as logging

threadsShouldRun = True


def mavControl(drone, commandQueue, mavLock):
    logging.info("mavControl started")
    mav_controller = mavioso.MAV_controller.MAVController(drone)
    global threadsShouldRun
    while threadsShouldRun:
        cmd = None
        try:
            cmd = commandQueue.get(True, 0.1)
        except Queue.Empty:
            pass
        mavLock.acquire()
        mav_controller.process(cmd)
        mavLock.release()

    logging.info("mavControl stopped")


def pathTracker(drone, mavLock):
    logging.info("pathTracker started")
    tracker = mavioso.PathTracker.PathTracker(drone)
    global threadsShouldRun
    while threadsShouldRun:
        mavLock.acquire()
        tracker.track()
        mavLock.release()
        time.sleep(0.01)

    logging.info("pathTracker stopped")


def main():
    Script.ChangeMode("GUIDED")

    drone = mavioso.MAV.MAV(Script, MAV, MAVLink, cs)

    mavLock = threading.Lock()

    mav_cmd_queue = Queue.Queue()

    control_thread = threading.Thread(target=mavControl, args=[drone, mav_cmd_queue, mavLock])
    # tracker_thread = threading.Thread(target=pathTracker, args=[drone, mavLock])

    try:
        control_thread.start()
        # tracker_thread.start()
        mavioso.http_server.run(drone, mav_cmd_queue, mavLock, 1234)

    except Exception as e:
        print(str(e))
        global threadsShouldRun
        threadsShouldRun = False
        control_thread.join()
        # tracker_thread.join()

main()
