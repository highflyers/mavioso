import mavioso.MAV
import mavioso.GeoCoordinate as GeoCoordinate
import time
import math
import logging

class PathTracker:
    def __init__(self, mav, cs):
        self.MAV = mav
        self.cs = cs
        self.current_waypoint = None
        self.current_waypoint_projection = None
        self.projection_distance = 100.0
        self.projection_change_distance = 10.0

    def track(self):
        if(self.cs.mode.upper() == "GUIDED"):
            if(self.MAV.next_goal != None):
                if(self.MAV.is_position_ok(self.MAV.next_goal)):
                    self.MAV.next_goal_reached = 1

            if(self.MAV.new_path):
                self.MAV.new_path = False
                if(len(self.MAV.path) > 0):
                    self.current_waypoint = GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.path[0])
                    self.current_waypoint_projection = self.calculateWaypointProjection(GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.currentstate()), self.current_waypoint)
                    self.MAV.path.pop(0)
                    if(len(self.MAV.path) > 0):
                        self.MAV.set_waypoint(self.current_waypoint_projection)
                    else:
                        self.MAV.set_waypoint(self.current_waypoint)

            if(self.current_waypoint != None):
                if(self.MAV.is_position_ok(self.current_waypoint)):
                    if(len(self.MAV.path) > 0):
                        self.current_waypoint = GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.path[0])
                        self.current_waypoint_projection = self.calculateWaypointProjection(GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.currentstate()), self.current_waypoint)
                        self.MAV.path.pop(0)
                        if(len(self.MAV.path) > 0):
                            self.MAV.set_waypoint(self.current_waypoint_projection)
                        else:
                            self.MAV.set_waypoint(self.current_waypoint)
                    else:
                        self.current_waypoint = None
                else:
                    wp_projection = self.calculateWaypointProjection(GeoCoordinate.GeoCoordinate.from_mav_state(self.MAV.currentstate()), self.current_waypoint)
                    if(wp_projection.distance_to(self.current_waypoint_projection) > self.projection_change_distance):
                        self.current_waypoint_projection = wp_projection
                        if(len(self.MAV.path) > 0):
                            self.MAV.set_waypoint(self.current_waypoint_projection)
                        else:
                            self.MAV.set_waypoint(self.current_waypoint)

    def calculateWaypointProjection(self, my_location, tgt_location):
        dlat = abs(tgt_location.latitude - my_location.latitude)*1852.0*60.0
        dlong = abs(tgt_location.longitude - my_location.longitude)*40075704.0*math.cos(tgt_location.latitude*3.14/180.0)/360.0

        if(dlong != 0):
            alpha = math.atan2(dlat, dlong)
            m_dlat = self.projection_distance*math.sin(alpha)
            m_dlon = self.projection_distance*math.cos(alpha)
        else:
            m_dlat = self.projection_distance
            m_dlon = 0.0

        if(tgt_location.latitude < my_location.latitude):
            m_dlat = -m_dlat
        if(tgt_location.longitude < my_location.longitude):
            m_dlon = -m_dlon

        dlat_p = m_dlat/(1852.0*60.0)
        dlon_p = m_dlon*360.0/(40075704.0*math.cos(tgt_location.latitude*3.14/180.0))

        return GeoCoordinate.GeoCoordinate(tgt_location.latitude+dlat_p, tgt_location.longitude+dlon_p, tgt_location.altitude)
