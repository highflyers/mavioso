import sys

sys.path.append(r"C:\Python27amd64\Lib")
sys.path.append(r"C:\maciej\projects\mavioso")

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


def stateConsumer(drone, mavLock):
    logging.info("stateConsumer started")
    global threadsShouldRun
    while threadsShouldRun:
        mavLock.acquire()
        # print(str(drone.currentstate()))
        mavLock.release()
        time.sleep(1)

    logging.info("stateConsumer stopped")


def main():
    Script.ChangeMode("GUIDED")

    drone = mavioso.MAV.MAV(Script, MAV, MAVLink, cs)

    mavLock = threading.Lock()

    mav_cmd_queue = Queue.Queue()

    control_thread = threading.Thread(target=mavControl, args=[drone, mav_cmd_queue, mavLock])
    consumer_thread = threading.Thread(target=stateConsumer, args=[drone, mavLock])

    try:
        control_thread.start()
        consumer_thread.start()
        mavioso.http_server.run(drone, mav_cmd_queue, mavLock, 6666)

    except Exception as e:
        print(str(e))
        global threadsShouldRun
        threadsShouldRun = False
        control_thread.join()
        consumer_thread.join()

main()
