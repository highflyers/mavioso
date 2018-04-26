import mavioso.MAV
import logging

class MAVController:
    def __init__(self, mav):
        self.MAV = mav

    def process(self, command=None):
        if(command is not None):
            if(len(command) == 2):
                logging.info("MAVController: process(): {0}".format(command[1]))
                function_kwargs = command[0]
                function_name = command[1]
                function_to_call = getattr(self.MAV, function_name)
                function_to_call(function_kwargs)
            else:
                logging.info("MAVController: process(): Bad command format")
        else:
            # logging.info("MAVController: process(): No command")
            pass
        pass
