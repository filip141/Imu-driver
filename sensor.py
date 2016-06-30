from abc import ABCMeta, abstractmethod

# Abstract class representing
# sensor objects
class Sensor(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def calibration(self):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @staticmethod
    def u2decode(arg):
        if len(bin(arg)) == 18:
            return -((~arg & 0xFFFF) + 1)
        else:
            return arg
