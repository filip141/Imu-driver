class Registers(object):
    WHO_AM_I_ADXL345 = 0x00         # Should return 0xE51
    ADXL345_THRESH_TAP = 0x1D       # Tap threshold
    ADXL345_OFSX = 0x1E             # X-axis offset
    ADXL345_OFSY = 0x1F             # Y-axis offset
    ADXL345_OFSZ = 0x20             # Z-axis offset
    ADXL345_DUR = 0x21              # Tap duration
    ADXL345_LATENT = 0x22           # Tap latency
    ADXL345_WINDOW = 0x23           # Tap window
    ADXL345_THRESH_ACT = 0x24       # Activity threshold
    ADXL345_THRESH_INACT = 0x25     # Inactivity threshold
    ADXL345_TIME_INACT = 0x26       # Inactivity time
    ADXL345_ACT_INACT_CTL = 0x27    # Axis enable control for activity/inactivity detection
    ADXL345_THRESH_FF = 0x28        # Free-fall threshold
    ADXL345_TIME_FF = 0x29          # Free-fall time
    ADXL345_TAP_AXES = 0x2A         # Axis control for single/double tap
    ADXL345_ACT_TAP_STATUS = 0x2B   # Source of single/double tap
    ADXL345_BW_RATE = 0x2C          # Data rate and power mode control
    ADXL345_POWER_CTL = 0x2D        # Power-saving features control
    ADXL345_INT_ENABLE = 0x2E       # Interrupt enable control
    ADXL345_INT_MAP = 0x2F          # Interrupt mapping control
    ADXL345_INT_SOURCE = 0x30       # Source of interrupts
    ADXL345_DATA_FORMAT = 0x31      # Data format control
    ADXL345_DATAX0 = 0x32           # X-axis data 0
    ADXL345_DATAX1 = 0x33           # X-axis data 1
    ADXL345_DATAY0 = 0x34           # Y-axis data 0
    ADXL345_DATAY1 = 0x35           # Y-axis data 1
    ADXL345_DATAZ0 = 0x36           # Z-axis data 0
    ADXL345_DATAZ1 = 0x37           # Z-axis data 1
    ADXL345_FIFO_CTL = 0x38         # FIFO control
    ADXL345_FIFO_STATUS = 0x39      # FIFO status
    ADXL345_ADDRESS = 0x53          # Device address when ADO = 0

BW_CODES = {
    3200: 0b1111,
    1600: 0b1110,
    800:  0b1101,
    400:  0b1100,
    200:  0b1011,
    100:  0b1010,
    50:   0b1001,
    25:   0b1000,
    12.5: 0b0111,
    6.25: 0b0110,
    3.13: 0b0101,
    1.56: 0b0100,
    0.78: 0b0011,
    0.39: 0b0010,
    0.20: 0b0001,
    0.10: 0b0000
}

# ADXL Range codes
RANGE_CODES = {
    2: 0b00,
    4: 0b01,
    8: 0b10,
    16: 0b11
}

SENSITIVITY = {
    0b00: 256,
    0b01: 128,
    0b10: 64,
    0b11: 32
}

SCALE_F = {
    0b00: 3.9,
    0b01: 7.8,
    0b10: 15.6,
    0b11: 31.2
}