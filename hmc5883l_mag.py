import smbus
import numpy as np
from sensor import Sensor
from display_fix import screen_fix
from hmc5883l_registers import Registers as HMC
from hmc5883l_registers import ODR_CODES, AW_CODES

screen_fix()


class HMC5883L(Sensor):

    dev_addr = HMC.HMC5883L_ADDRESS

    def __init__(self, i2c_port):
        self.i2c_bus = smbus.SMBus(i2c_port)
        self.set_odr(75)
        self.samples_averaged(8)

    # Set sensor output data rate
    def set_odr(self, user_odr):
        if user_odr in ODR_CODES.keys():
            self.i2c_bus.write_byte(self.dev_addr, HMC.HMC5883L_CONFIG_A)
            conf_rega = self.i2c_bus.read_byte(self.dev_addr)
            conf_rega |= ODR_CODES[user_odr] << 2
            self.i2c_bus.write_byte_data(self.dev_addr, HMC.HMC5883L_CONFIG_A, conf_rega)
        else:
            raise ValueError("Wrong Output Data Rate for HMC Sensor Check Table 5. p.11")

    def samples_averaged(self, nsamples):
        if nsamples in AW_CODES.keys():
            self.i2c_bus.write_byte(self.dev_addr, HMC.HMC5883L_CONFIG_A)
            conf_rega = self.i2c_bus.read_byte(self.dev_addr)
            conf_rega |= AW_CODES[nsamples] << 5
            self.i2c_bus.write_byte_data(self.dev_addr, HMC.HMC5883L_CONFIG_A, conf_rega)
        else:
            raise ValueError("Wrong number of samples averaged Check Table 4. p.11")

    def read_data(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def calibration(self):
        pass


def main():
    mag = HMC5883L(1)

if __name__ == '__main__':
    main()