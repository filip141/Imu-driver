class Registers(object):
    HMC5883L_ADDRESS = 0x1E
    HMC5883L_CONFIG_A = 0x00
    HMC5883L_CONFIG_B = 0x01
    HMC5883L_MODE = 0x02
    HMC5883L_OUT_X_H = 0x03
    HMC5883L_OUT_X_L = 0x04
    HMC5883L_OUT_Z_H = 0x05
    HMC5883L_OUT_Z_L = 0x06
    HMC5883L_OUT_Y_H = 0x07
    HMC5883L_OUT_Y_L = 0x08
    HMC5883L_STATUS = 0x09
    HMC5883L_IDA = 0x0A
    HMC5883L_IDB = 0x0B
    HMC5883L_IDC = 0x0C


ODR_CODES = {
    0.75: 0b000,
    1.5: 0b001,
    3.0: 0b010,
    7.5: 0b011,
    15.0: 0b100,
    30.0: 0b101,
    75.0: 0b110
}

AW_CODES = {
    1: 0b00,
    2: 0b01,
    4: 0b10,
    8: 0b11
}