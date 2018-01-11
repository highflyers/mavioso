import mavioso.MAV
import logging

class MAVController:
    def __init__(self, mav):
        self.MAV = mav

    def process(self, command=None):
        if(command is not None):
            logging.info("MAVController: process(): {0}".format(str(command)))
            # TODO: implement
        else:
            # logging.info("MAVController: process(): No command")
            pass
        pass
