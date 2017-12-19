class MaviosoException(Exception):
    def __init__(self, message):
        self.message = message


class WrongModeException(MaviosoException):
    pass


class NotArmedException(MaviosoException):
    pass


class AlreadyInAirException(MaviosoException):
    pass
