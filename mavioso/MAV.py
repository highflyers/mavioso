import logging

from MissionPlanner.Utilities import Locationwp

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
        status = self.mav.doARM(True)
        logging.info("MAV: arm(): {0}".format(status))
        return status

    def disarm(self):
        status = self.mav.doARM(False)
        logging.info("MAV: disarm(): {0}".format(status))
        return status

    def takeoff(self, alt):
        status = self.mav.doCommand(self.mavlink.MAV_CMD.TAKEOFF, 0, 0, 0, 0, 0, 0, float(alt))
        logging.info("takeoff {0}".format(status))
        return status

    def set_waypoint(self, coordinate):
        # TODO: it probably does not like coordinate argument that equals 0.0. Setting it to 0.01 works fine
        wp1 = Locationwp().Set(coordinate.latitude, coordinate.longitude, coordinate.altitude,
                               int(self.mavlink.MAV_CMD.WAYPOINT))
        self.mav.setGuidedModeWP(wp1, True)
        logging.info("MAV: set_waypoint() {0}".format(str(coordinate)))
