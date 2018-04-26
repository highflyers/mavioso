import mavioso.MAV
import mavioso.GeoCoordinate as GeoCoordinate
import time

class PathTracker:
    def __init__(self, mav):
        self.MAV = mav
        self.current_waypoint = None

    def track(self):
        if(self.MAV.new_path):
            self.MAV.new_path = False
            if(len(self.MAV.path) > 0):
                self.current_waypoint = GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.path[0])
                self.MAV.path.pop(0)
                self.MAV.set_waypoint(self.current_waypoint)

        if(self.current_waypoint != None):
            if(self.MAV.is_position_ok(self.current_waypoint)):
                if(len(self.MAV.path) > 0):
                    self.current_waypoint = GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.path[0])
                    self.MAV.path.pop(0)
                    self.MAV.set_waypoint(self.current_waypoint)
                else:
                    self.current_waypoint = None
        time.sleep(0.01)
