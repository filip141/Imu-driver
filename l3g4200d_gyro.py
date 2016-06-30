import time
import smbus
import numpy as np
from datetime import datetime
from display_fix import screen_fix
from sensor import Sensor
from l3g4200d_registers import Registers as L3G4
from l3g4200d_registers import BW_CODES, SCALE_SEL,\
    DPS_Per_Digit
import matplotlib.pyplot as plt

screen_fix()


class L3G4Gyro(Sensor):

    dev_addr = L3G4.L3G4200D_ADDRESS

    def __init__(self, i2c_port, odr=100, cut_off=12.5, scale=2000):
        super(L3G4Gyro, self).__init__()
        self.scale = scale
        self.gyro_off = [0, 0, 0]
        self.i2c_bus = smbus.SMBus(i2c_port)
        self.reset()
        self.bandwidth(odr, cut_off)
        self.scale_selection(scale)
        self.cal_mean, self.var_noise = self.calibration()

    def scale_selection(self, scale):
        self.scale = scale
        if scale in SCALE_SEL.keys():
            selected = SCALE_SEL[scale]
            self.i2c_bus.write_byte_data(self.dev_addr, L3G4.L3G4200D_CTRL_REG4, selected << 4)
        else:
            raise ValueError("Wrong scale selected look at page 32, table 30.")

    # Set output data rate
    def bandwidth(self, odr, cut_off):
        if odr in BW_CODES.keys():
            cuts = BW_CODES[odr]
            if cut_off in cuts.keys():
                self.i2c_bus.write_byte_data(self.dev_addr,
                                             L3G4.L3G4200D_CTRL_REG1,
                                             cuts[cut_off] << 4 | 0x0F)
            else:
                raise ValueError("Wrong cut-off frequency look at page 29, table 22 in datasheet")
        else:
            raise ValueError("Wrong ODR look at page 29, table 22 in datasheet")

    # reset gyro
    def reset(self):
        self.turn_off()
        time.sleep(0.01)
        self.turn_on()

    # turn off gyroscope
    def turn_off(self):
        self.i2c_bus.write_byte_data(self.dev_addr, L3G4.L3G4200D_CTRL_REG5, 0x80)
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_CTRL_REG1)
        status_reg1 = self.i2c_bus.read_byte(self.dev_addr) & 0xF0
        self.i2c_bus.write_byte_data(self.dev_addr, L3G4.L3G4200D_CTRL_REG1, status_reg1)

    # turn on gyroscope
    def turn_on(self):
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_CTRL_REG1)
        status_reg1 = self.i2c_bus.read_byte(self.dev_addr) | 0x0F
        self.i2c_bus.write_byte_data(self.dev_addr, L3G4.L3G4200D_CTRL_REG1, status_reg1)
        self.i2c_bus.write_byte_data(self.dev_addr, L3G4.L3G4200D_CTRL_REG5, 0x00)

    def calibration(self):
        n = 0
        u_ml = [0, 0, 0]
        var_ml = [0, 0, 0]
        var_arr = []
        while n < 1100:
            self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_STATUS_REG)
            status = self.i2c_bus.read_byte(self.dev_addr) & 0x08
            if status:
                coords = self.read_data()
                n += 1
                if n > 100:
                    n_points = n - 100
                    coords = np.array(coords)
                    u_ml += (1.0 / n_points) * (coords - u_ml)
                    var_ml += (1.0 / n_points) * ((coords - u_ml)**2 - var_ml)
                    var_arr.append(var_ml)
        var_noise = np.mean(var_arr, axis=0)
        var_noise = (var_noise[0], var_noise[1], var_noise[2])
        return u_ml, var_noise

    def read_data(self):
        coords = [0, 0, 0]
        # Read x sample
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_X_L)
        gyro_x0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_X_H)
        gyro_x1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[0] = self.u2decode((gyro_x1 << 8) | gyro_x0)
        # Read y sample
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_Y_L)
        gyro_y0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_Y_H)
        gyro_y1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[1] = self.u2decode((gyro_y1 << 8) | gyro_y0)

        # Read z sample
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_Z_L)
        gyro_z0 = self.i2c_bus.read_byte(self.dev_addr)
        self.i2c_bus.write_byte(self.dev_addr, L3G4.L3G4200D_OUT_Z_H)
        gyro_z1 = self.i2c_bus.read_byte(self.dev_addr)
        coords[2] = self.u2decode((gyro_z1 << 8) | gyro_z0)

        # Remove offset
        coords[0] = (coords[0] - self.gyro_off[0]) * DPS_Per_Digit[self.scale]
        coords[1] = (coords[1] - self.gyro_off[1]) * DPS_Per_Digit[self.scale]
        coords[2] = (coords[2] - self.gyro_off[2]) * DPS_Per_Digit[self.scale]
        return coords

    def read_filter(self, varparam=3):
        var_noise = [k * varparam**2 for k in self.var_noise]
        coordinates = self.read_data()
        coordinates = np.array(coordinates)
        var_mom = ((coordinates - self.cal_mean)**2).tolist()
        coordinates = [coordinates[i] - self.cal_mean[i]
                       if var_mom[i] > var_noise[i]
                       else 0 for i in range(0, 3)
                       ]
        return coordinates

    def read_in_loop(self):
        pointsx = []
        pointsy = []
        pointsz = []
        gz = 0
        start = datetime.now().microsecond
        while True:
            coordinates = self.read_filter()
            print " x: " + str(coordinates[0]),
            print " y: " + str(coordinates[1]),
            print " z: " + str(coordinates[2]),
            pointsx.append(coordinates[0])
            pointsy.append(coordinates[1])
            pointsz.append(coordinates[2])
            gz += coordinates[2] * 1/100.0
            print gz
            time_in_loop = datetime.now().microsecond - start
            if time_in_loop < 10000:
                while time_in_loop < 10000:
                    time_in_loop = datetime.now().microsecond - start
                    if time_in_loop < 0:
                        time_in_loop = datetime.now().microsecond + (1000000 - start)
            start = datetime.now().microsecond
        # plt.plot(pointsx, 'r')
        # plt.plot(pointsy, 'b')
        # plt.plot(pointsz, 'g')
        # plt.show()


def main():
    gyro = L3G4Gyro(1)
    gyro.read_in_loop()

if __name__ == '__main__':
    main()