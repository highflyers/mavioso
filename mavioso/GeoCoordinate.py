import math

class GeoCoordinate:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)

    """ Returns distance to another coordinate in meters"""
    def distance_to(self, other):
        dlat = abs(other.latitude - self.latitude)*1852.0*60.0
        dlong = abs(other.longitude - self.longitude)*40075704.0*math.cos(self.latitude*3.14/180.0)/360.0
        diff_tot = math.sqrt(math.pow(dlat,2) + math.pow(dlong,2))
        return diff_tot

    def __str__(self):
        string = "{0} {1} {2}".format(self.latitude, self.longitude, self.altitude)
        return string

    @staticmethod
    def from_mav_state(mav_state):
        coord = GeoCoordinate(mav_state["latitude"], mav_state["longitude"], mav_state["altitude"])
        return coord
