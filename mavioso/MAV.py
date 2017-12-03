import logging
import time

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
        self.position_check_threshold = 50


    def currentstate(self):
        """Return current state as dictionary"""
        ret = {"latitude": float(self.cs.lat), "longitude": float(self.cs.lng), "altitude": float(self.cs.alt)}
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
        if self.cs.armed is False:
            raise mavioso.MaviosoExceptions.NotArmedException('Takeoff failed, UAV is not armed')
        if self.cs.mode.upper() != 'GUIDED':
            raise mavioso.MaviosoExceptions.WrongModeException('Takeoff failed, expected mode is GUIDED,'
                                     + ' current mode is {0}'.format(self.cs.mode))
        status = self.mav.doCommand(self.mavlink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, float(alt))
        logging.info("takeoff {0}".format(status))
        if status is False:
            raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while taking off')
        return status

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
        status = self.mav.setMode(mode)
        return status

    def set_VTOL_mode(self, quadmode):
        """Put MAV into quadrotor or plane mode
        :param quadmode: mode to set (1 for quadrotor, 0 for plane)"""
        self.mav.setParam("Q_GUIDED_MODE", quadmode)
        wp1 = Locationwp().Set(self.cs.lat, self.cs.lng, self.cs.alt, int(self.mavlink.MAV_CMD.WAYPOINT))
        self.mav.setGuidedModeWP(wp1, True)
        logging.info("MAV: VTOL mode: {0}".format(quadmode))

    def set_circle_radius(self, radius):            #set circle radius in loiter and guided (circles after reaching the waypoint) mode
        status = self.mav.setParam("WP_LOITER_RAD", radius)
        logging.info("set radius to {0}: {1}".format(radius, status))
