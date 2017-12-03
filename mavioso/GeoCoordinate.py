class GeoCoordinate:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)

    def __str__(self):
        string = "{0} {1} {2}".format(self.latitude, self.longitude, self.altitude)
        return string

    @staticmethod
    def from_mav_state(mav_state):
        coord = GeoCoordinate(mav_state.latitude, mav_state.longitude, mav_state.altitude)
        return coord
