import math

class GeoCoordinate:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)

    """ Returns distance to another coordinate in meters"""
    def distance_to(self, other):
        diff_lat = other.latitude - self.latitude
        diff_lat = (111132.954 - 559.822 * math.cos(2 * self.latitude) + 1.175 * math.cos(4 * self.latitude))*diff_lat
        diff_lon = (other.longitude - self.longitude)
        diff_lon = 111132.954 * math.cos(self.latitude) * diff_lon
        diff_alt = (other.altitude - self.altitude)
        diff_lat = math.pow(diff_lat, 2)
        diff_lon = math.pow(diff_lon, 2)
        diff_alt = math.pow(diff_alt, 2)
        diff_tot = math.sqrt(diff_lat + diff_lon + diff_alt)
        return diff_tot

    def __str__(self):
        string = "{0} {1} {2}".format(self.latitude, self.longitude, self.altitude)
        return string

    @staticmethod
    def from_mav_state(mav_state):
        coord = GeoCoordinate(mav_state["latitude"], mav_state["longitude"], mav_state["altitude"])
        return coord
