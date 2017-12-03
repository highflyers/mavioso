import logging

from MissionPlanner.Utilities import Locationwp

import mavioso.MaviosoExceptions

class MAV:
    def __init__(self, Script, MAV, MAVLink, cs):
        self.script = Script
        self.mav = MAV
        self.mavlink = MAVLink
        self.cs = cs

    def currentstate(self):
        ret = {"lat": float(self.cs.lat), "lng": float(self.cs.lng), "alt": float(self.cs.alt)}
        return ret

    def arm(self):
        if self.cs.armed:
            logging.info("Already armed, ignoring command...")
            return False
        status = self.mav.doARM(True)
        logging.info("MAV: arm(): {0}".format(status))
        if status is False:
            raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while arming')
        return status

    def disarm(self):
        if self.cs.armed is False:
            logging.info("Already disarmed, ignoring command...")
            return False
        status = self.mav.doARM(False)
        logging.info("MAV: disarm(): {0}".format(status))
        if status is False:
            raise mavioso.MaviosoExceptions.MaviosoException('unexpected error while disarming')
        return status

    def takeoff(self, alt):
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

    def set_waypoint(self, coordinate):
        wp1 = Locationwp().Set(coordinate.latitude, coordinate.longitude, coordinate.altitude,
                               int(self.mavlink.MAV_CMD.WAYPOINT))
        self.mav.setGuidedModeWP(wp1, True)

    def set_mode(self, mode):
        status = self.mav.setMode(mode)
        return status

    def q_loiter(self):
        self.mav.setParam("Q_GUIDED_MODE", 1)       #when the loiter is ended, we have to remember to change Q_GUIDED_MODE to 0, if we want it to be 0
        wp1 = Locationwp().Set(self.cs.lat, self.cs.lng, self.cs.alt, int(self.mavlink.MAV_CMD.WAYPOINT))
        self.mav.setGuidedModeWP(wp1, True)
        logging.info("qloiter")

    def set_circle_radius(self, radius):            #set circle radius in loiter and guided (circles after reaching the waypoint) mode
        status = self.mav.setParam("WP_LOITER_RAD", radius)
        logging.info("set radius to {0}: {1}".format(radius, status))