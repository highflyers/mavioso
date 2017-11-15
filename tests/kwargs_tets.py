class MAV:
    def __init__(self):
        pass

    def currentstate(self):
        print("currentstate()")

    def arm(self):
        print("arm()")

    def disarm(self):
        print("disarm()")

    def takeoff(self, **kwargs):
        print("takeoff({0})".format(kwargs.items()))

    def set_waypoint(self, coordinate):
        print("set_waypoint({0})".format(coordinate))

def main():
    drone = MAV()
    drone.arm()
    getattr(drone, "arm")()
    drone.takeoff(alt=50)
    drone.takeoff(**{"alt": float(50)})

if __name__ == '__main__':
    main()