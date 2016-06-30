import smbus
import time
from sensor import Sensor
from adxl_registers import Registers as ADXL
from adxl_registers import BW_CODES, RANGE_CODES,\
    SENSITIVITY, SCALE_F


# Driver for ADXL345 accelerometer
class ADXLAccel(Sensor):

    dev_addr = ADXL.ADXL345_ADDRESS

    def __init__(self, i2c_port, g_range, data_rate, full_res=True):
        self.g_range = g_range
        self.data_rate = data_rate
        self.full_res = full_res
        self.i2c_bus = smbus.SMBus(i2c_port)
        self.reset()
        self.data_format(g_range, fullres=full_res)
        self.bandwidth(data_rate, lp_mode=False)
        self.calibration()

    # Set accelerometer data format
    # g range and resolution
    def data_format(self, g_range, fullres=True):
        if g_range in RANGE_CODES.keys():
            val = RANGE_CODES[g_range]
            self.g_range = g_range
            self.full_res = fullres
            if fullres:
                reg_val = val | (1 << 3)
                self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_DATA_FORMAT, reg_val)
            else:
                self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_DATA_FORMAT, val)
        else:
            raise ValueError("Not allowed range value !")

    # Set accelerometer bandwidth, allowed values could be found
    # in Table 7. in Datasheet
    def bandwidth(self, data_rate, lp_mode=False):
        if data_rate in BW_CODES.keys():
            code = BW_CODES[data_rate]
            self.data_rate = data_rate
            if lp_mode:
                reg_val = (code | (1 << 4))
                self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_BW_RATE, reg_val)
            else:
                self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_BW_RATE, code)
        else:
            raise ValueError("Wrong frequency, check datasheet Table 7!")

    # Reset accelerometer
    def reset(self):
        self.turn_off()
        time.sleep(0.01)
        self.turn_on()

    # Turn off accelerometer
    def turn_off(self):
        self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_POWER_CTL, 0x00)

    # Turn on accelerometer
    def turn_on(self):
        self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_POWER_CTL, 0x08)

    # Accelerometer calibration process
    def calibration(self):
        if self.full_res:
            accelsensitivity = 256
        else:
            accelsensitivity = SENSITIVITY[RANGE_CODES[self.g_range]]
        self.i2c_bus.write_byte_data(self.dev_addr, ADXL.ADXL345_FIFO_CTL, 0x5F)
        time.sleep(0.33)
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_FIFO_STATUS)
        fifo_samples = self.i2c_bus.read_byte(self.dev_addr)
        coords = [0, 0, 0]
        for n in range(0, fifo_samples):
            # Read x sample
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAX0)
            accel_x0 = self.i2c_bus.read_byte(self.dev_addr)
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAX1)
            accel_x1 = self.i2c_bus.read_byte(self.dev_addr)
            coords[0] += self.u2decode((accel_x1 << 8) | accel_x0)
            # Read y sample
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAY0)
            accel_y0 = self.i2c_bus.read_byte(self.dev_addr)
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAY1)
            accel_y1 = self.i2c_bus.read_byte(self.dev_addr)
            coords[1] += self.u2decode((accel_y1 << 8) | accel_y0)

            # Read z sample
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAZ0)
            accel_z0 = self.i2c_bus.read_byte(self.dev_addr)
            self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAZ1)
            accel_z1 = self.i2c_bus.read_byte(self.dev_addr)
            coords[2] += self.u2decode((accel_z1 << 8) | accel_z0)

        # Average samples
        coords[0] /= fifo_samples
        coords[1] /= fifo_samples
        coords[2] /= fifo_samples

        # Remove gravity from z-axis accelerometer bias value
        if coords[2] > 0:
            coords[2] -= accelsensitivity
        else:
            coords[2] += accelsensitivity

        coords[0] = int(-coords[0] / 4.0)
        coords[1] = int(-coords[1] / 4.0)
        coords[2] = int(-coords[2] / 4.0)

        self.i2c_bus.write_byte_data(self.dev_addr,
                                     ADXL.ADXL345_OFSX, coords[0])
        self.i2c_bus.write_byte_data(self.dev_addr,
                                     ADXL.ADXL345_OFSY, coords[1])
        self.i2c_bus.write_byte_data(self.dev_addr,
                                     ADXL.ADXL345_OFSZ, coords[2])
        self.i2c_bus.write_byte_data(self.dev_addr,
                                     ADXL.ADXL345_FIFO_CTL, 0x00)

    def read_data(self):
        if self.full_res:
            scale_factor = 3.9 / 1000.0
        else:
            scale_factor = SCALE_F[RANGE_CODES[self.g_range]] / 1000.0

        coords = [0, 0, 0]
        # Read x sample
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAX0)
        accel_x0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAX1)
        accel_x1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[0] += self.u2decode((accel_x1 << 8) | accel_x0)

        # Read y sample
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAY0)
        accel_y0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAY1)
        accel_y1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[1] += self.u2decode((accel_y1 << 8) | accel_y0)

        # Read z sample
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAZ0)
        accel_z0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, ADXL.ADXL345_DATAZ1)
        accel_z1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[2] += self.u2decode((accel_z1 << 8) | accel_z0)
        return [param*scale_factor for param in coords]

    def read_sequentially(self):
        while True:
            coordinates = self.read_data()
            print " x: " + str(coordinates[0]),
            print " y: " + str(coordinates[1]),
            print " z: " + str(coordinates[2])


def main():
    acc = ADXLAccel(1, 16, 100)
    acc.read_sequentially()

if __name__ == '__main__':
    main()
