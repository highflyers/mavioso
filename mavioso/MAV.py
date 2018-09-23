import logging
import time
import json

from MissionPlanner.Utilities import Locationwp

import mavioso.MaviosoExceptions
import mavioso.GeoCoordinate as GeoCoordinate

WAIT_WAYPOINT_SLEEP_TIME = 500
VTOL_MODE_PLANE = 0
VTOL_MODE_QUAD = 1

class MAV:
    def __init__(self, Script, MAV, MAVLink, cs):
        self.script = Script
        self.mav = MAV
        self.mavlink = MAVLink
        self.cs = cs
        self.position_check_threshold = 40
        self.path = []
        self.new_path = False
        self.current_waypoint = None
        self.next_goal = None
        self.next_goal_reached = 0
        self.vtol_flight = False
        self.control_on = True

    def currentstate(self):
        logging.info("Datetime: {0}".format(self.cs.datetime))
        """Return current state as dictionary"""
        ret = {"latitude": float(self.cs.lat), "longitude": float(self.cs.lng), "altitude": float(self.cs.alt),
        "groundSpeed": float(self.cs.groundspeed), "heading": float(self.cs.yaw), "airspeed": float(self.cs.airspeed)}
        return ret

    def currentMode(self):
        """Return platform current mode"""
        ret = {"mode": self.cs.mode.upper()}
        return ret;

    def nextGoalState(self):
        """Return info if next goal reached"""
        ret = {"reached": int(self.next_goal_reached)}
        return ret

    def isArmed(self):
        armed = 0
        if(self.cs.armed):
            armed = 1
        ret = {"armed": armed}
        return ret

    def getRuntime(self):
        try:
            logging.info("MAV: Reading runtime")
            # ret = {"runtime": float(self.mav.GetParam("STAT_RUNTIME"))}
            ret = {"time_in_air": self.cs.rxrssi}
            logging.info("MAV: getRuntime(): {0}".format(ret))
        except:
            ret = {"runtime": -2.0}
        return ret

    def arm(self):
        """Arm MAV
        :return True on success, False if MAV is already armed"""
        if self.cs.armed:
            logging.info("Already armed, ignoring command...")
            return False
        status = self.mav.doARM(True)
        logging.info("MAV: arm(): {0}".format(status))
        if status is False:
            raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while arming')
        return status

    def disarm(self):
        """Disarm MAV
        :return True on success, False if MAV is already disarmed"""
        if self.cs.armed is False:
            logging.info("Already disarmed, ignoring command...")
            return False
        status = self.mav.doARM(False)
        logging.info("MAV: disarm(): {0}".format(status))
        if status is False:
            raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while disarming')
        return status

    def takeoff(self, alt):
        """Issue Takeoff command
        :param alt: Altitude to be obtained after takeoff (no horizontal movement is assumed)
        :return True on success, False otherwise"""
        logging.info("Starting takeoff")
        data = json.loads(alt)
        altitude = data['altitude']
        if self.cs.mode.upper() != "GUIDED":
            self.set_mode("GUIDED")
            while(self.cs.mode.upper != "GUIDED"):
                time.sleep(0.1)

        if self.cs.armed is False:
            self.arm()
            while(not self.cs.armed):
                time.sleep(0.1)
        
        status = self.mav.doCommand(self.mavlink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, float(altitude))
        logging.info("takeoff {0}".format(status))
        # if status is False:
            # raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while taking off')
        return status

    def set_next_goal(self, coordinate, timeout=-1):
        """Set new goal waypoint"""
        self.next_goal = GeoCoordinate.GeoCoordinate.from_mav_state(json.loads(coordinate))
        self.next_goal_reached = 0
        logging.info("MAV: set_next_goal() {0}".format(str(coordinate)))
        return 1

    def set_waypoint(self, coordinate, should_wait=False, timeout=-1):
        """Set GUIDED mode waypoint
        :param coordinate: GeoCoordinate object describing waypoint
        :param should_wait: (bool) Wait until waypoint is reached? (Basing on is_position_ok function)
        :param timeout: timeout in seconds (works if should_wait is True): -1 to disable"""
        # TODO: it probably does not like coordinate argument that equals 0.0. Setting it to 0.01 works fine
        wp1 = Locationwp().Set(coordinate.latitude, coordinate.longitude, coordinate.altitude,
                               int(self.mavlink.MAV_CMD.WAYPOINT))
        self.mav.setGuidedModeWP(wp1, True)
        logging.info("MAV: set_waypoint() {0}".format(str(coordinate)))
        timeout_occurred = False
        if should_wait:
            timeout_occurred = self.wait_waypoint(coordinate, timeout=timeout)
        return timeout_occurred


    def wait_waypoint(self, coordinate, threshold=None, timeout=-1):
        """Wait until MAV reaches specified waypoint
        :param coordinate: GeoCoordinate object, a waypoint to check
        :param threshold: maximal distance from waypoint to assume waypoint is reached
        :param timeout: timeout in seconds (-1 to disable)"""
        time_begin = time.time()
        timeout_occurred = False
        while not(self.is_position_ok(coordinate, threshold)):
            self.script.Sleep(WAIT_WAYPOINT_SLEEP_TIME)
            current_time = time.time()
            if (timeout > 0) and (current_time - time_begin) > timeout:
                timeout_occurred = True
                break
        return timeout_occurred

    def is_position_ok(self, coordinate, threshold=None):
        """Check if MAV is within range of specified coordinate"""
        thr = self.position_check_threshold
        if threshold is not None:
            thr = threshold
        current_pos = GeoCoordinate.GeoCoordinate.from_mav_state(self.currentstate())
        dist = coordinate.distance_to(current_pos)
        logging.debug("MAV: is_position_ok: distance = {0}".format(dist))
        return dist < thr

    def set_mode(self, mode):
        logging.debug("MAV: set_mode: "+mode)
        try:
            data = json.loads(mode)
            parsedMode = data['mode']
            if(parsedMode == "AUTO"):
                self.control_on = False
                self.path = []
                self.current_waypoint = None
                self.next_goal = None
                # self.mav.setWPTotal(2)
                # home = Locationwp().Set(50.26670,18.670729,0, int(self.mavlink.MAV_CMD.WAYPOINT)) #to do: read current home
                # self.mav.setWP(home,0,self.mavlink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
                # loiter = Locationwp()
                # Locationwp.id.SetValue(loiter, int(self.mavlink.MAV_CMD.LOITER_UNLIM))
                # Locationwp.alt.SetValue(loiter, 30)
                # self.mav.setWP(loiter, 1, self.mavlink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

                # self.mav.setWPACK();
                # self.mav.setWPCurrent(1)

                # self.control_on = True

            if(parsedMode == "GUIDED"):
                logging.info("MAV: set control on to True")
                self.control_on = True

            status = self.mav.setMode(parsedMode)
        except:
            status = self.mav.setMode(mode)

        logging.debug("MAV: mode: {0}".format(self.cs.mode))
        return status

    def start_loiter(self, arg):
        self.path = []
        self.current_waypoint = None
        self.set_mode("Loiter")

    def enable_control(self, isEnabled):
        try:
            data = json.loads(mode)
            enabled = data['isEnabled']
            if(enabled == 1):
                self.control_on = True
            else:
                self.control_on = False
        except:
            if(isEnabled == 1):
                self.control_on = True
            else:
                self.control_on = False

    def set_VTOL_mode(self, quadmode):
        if(self.vtol_flight == True):
            """Put MAV into quadrotor or plane mode
            :param quadmode: mode to set (1 for quadrotor, 0 for plane)"""
            self.mav.setParam("Q_GUIDED_MODE", quadmode)
            # wp1 = Locationwp().Set(self.cs.lat, self.cs.lng, self.cs.alt, int(self.mavlink.MAV_CMD.WAYPOINT))
            # self.mav.setGuidedModeWP(wp1, True)
            logging.info("MAV: VTOL mode: {0}".format(quadmode))

    def set_circle_radius(self, radius):            #set circle radius in loiter and guided (circles after reaching the waypoint) mode
        status = self.mav.setParam("WP_LOITER_RAD", radius)
        logging.info("set radius to {0}: {1}".format(radius, status))
        return status

    def set_path(self, path):
        try:
            logging.info("control on: {0}, mode: {1}".format(self.control_on, self.cs.mode.upper()))
            if(self.control_on == True and self.cs.mode.upper() == "GUIDED"):
                data = json.loads(path)
                self.path = data['waypoints']
                self.new_path = True
                logging.info("MAV: set_path() {0}".format(self.path))
                # self.setAutoMission()
            else:
                logging.warning("MAV: trying to set path while not in GUIDED mode")
        except:
            logging.info("MAV: set_path(): Error while setting path")
            return 0
        return 1

    def setAutoMission(self):
        if(self.control_on == True and self.cs.mode.upper() != "GUIDED" and self.cs.mode.upper() != "BRAKE" and self.cs.mode.upper() != "LAND"):
            """Set auto mission from current path"""
            home = Locationwp().Set(50.26670,18.670729,0, int(self.mavlink.MAV_CMD.WAYPOINT)) #to do: read current home

            max_wp_total = 5

            if(len(self.path) > max_wp_total):
                wp_total = max_wp_total+2
            else:
                wp_total = len(self.path)+2

            self.mav.setWPTotal(wp_total)

            logging.info("MAV: setAutoMission: total wps count = {0}".format(len(self.path)+1))
            self.mav.setWP(home,0,self.mavlink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

            counter = 1
            for i in self.path:
                next_wp = GeoCoordinate.GeoCoordinate.from_mav_state(i)
                wp = Locationwp().Set(next_wp.latitude,next_wp.longitude,30, int(self.mavlink.MAV_CMD.WAYPOINT))
                logging.info("MAV: set_auto_mission(): set_wp: {0}, {1}".format(next_wp.latitude, next_wp.longitude))
                self.mav.setWP(wp,counter,self.mavlink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
                counter+=1
                if(counter > max_wp_total):
                    break

            loiter = Locationwp()
            Locationwp.id.SetValue(loiter, int(self.mavlink.MAV_CMD.LOITER_UNLIM))
            Locationwp.alt.SetValue(loiter, 30)
            self.mav.setWP(loiter, counter, self.mavlink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

            self.mav.setWPACK();

            self.set_mode("GUIDED")
            self.mav.setWPCurrent(1)
            self.set_mode("AUTO")
