class Registers(object):
    WHO_AM_I_L3G4200D = 0x0F  # Should return 0xD3
    L3G4200D_CTRL_REG1 = 0x20
    L3G4200D_CTRL_REG2 = 0x21
    L3G4200D_CTRL_REG3 = 0x22
    L3G4200D_CTRL_REG4 = 0x23
    L3G4200D_CTRL_REG5 = 0x24
    L3G4200D_REFERENCE = 0x25
    L3G4200D_OUT_TEMP = 0x26
    L3G4200D_STATUS_REG = 0x27
    L3G4200D_OUT_X_L = 0x28
    L3G4200D_OUT_X_H = 0x29
    L3G4200D_OUT_Y_L = 0x2A
    L3G4200D_OUT_Y_H = 0x2B
    L3G4200D_OUT_Z_L = 0x2C
    L3G4200D_OUT_Z_H = 0x2D
    L3G4200D_FIFO_CTRL_REG = 0x2E
    L3G4200D_FIFO_SRC_REG = 0x2F
    L3G4200D_INT1_CFG = 0x30
    L3G4200D_INT1_SRC = 0x31
    L3G4200D_INT1_TSH_XH = 0x32
    L3G4200D_INT1_TSH_XL = 0x33
    L3G4200D_INT1_TSH_YH = 0x34
    L3G4200D_INT1_TSH_YL = 0x35
    L3G4200D_INT1_TSH_ZH = 0x36
    L3G4200D_INT1_TSH_ZL = 0x37
    L3G4200D_INT1_DURATION = 0x38
    L3G4200D_ADDRESS = 0x69  # Device address when ADO = 0


BW_CODES = {
    100: {
        12.5: 0b0000,
        25: 0b0001,
        25: 0b0010,
        25: 0b0011
    },
    200: {
        12.5: 0b0100,
        25: 0b0101,
        50: 0b0110,
        70: 0b0111
    },
    400: {
        20: 0b1000,
        25: 0b1001,
        50: 0b1010,
        110: 0b1011
    },
    800: {
        30: 0b1100,
        35: 0b1101,
        50: 0b1110,
        110: 0b1111
    }
}


SCALE_SEL = {
    250: 0b00,
    500: 0b01,
    2000: 0b11,
}

DPS_Per_Digit = {
    250: .00875,
    500: .0175,
    2000: .07
}