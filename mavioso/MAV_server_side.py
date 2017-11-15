class MAV_server_side:
    def __init__(self, MAV):
        self.mav = MAV

    def currentstate(self):
        return self.mav.currentstate()

    def arm(self, **kwargs):
        return self.mav.arm()

    def disarm(self, **kwargs):
        return self.mav.disarm()

    def takeoff(self, **kwargs):
        return self.mav.takeoff(kwargs["alt"])

    def set_waypoint(self, **kwargs):
        return self.mav.set_waypoint(kwargs["coordinate"])
