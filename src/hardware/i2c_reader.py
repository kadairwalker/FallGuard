
import time
import smbus2

# --- MMA7660FC register map, confirmed against the NXP datasheet ---
I2C_ADDRESS = 0x4C      # fixed for this chip -- no AD0 pin to configure, unlike MPU6050
MODE_REG = 0x07         # write here to wake the chip up
MODE_ACTIVE = 0x01      # the chip boots in Standby mode and stays silent until this is set
XOUT_REG = 0x00         # X, Y, Z are three SEPARATE single-byte registers, back to back
YOUT_REG = 0x01
ZOUT_REG = 0x02
ALERT_BIT = 0x40        # bit 6 -- set if this byte was caught mid-update, meaning it may be torn/invalid
SIGN_BIT = 0x20         # bit 5 -- the sign bit within the 6-bit value
VALUE_MASK = 0x3F       # bits 0-5 -- the actual 6-bit measurement
ACCEL_SCALE = 21.33     # counts per g, confirmed against two independent real driver
                        # implementations for this exact chip. Still worth a sanity check
                        # once wired up: lay the sensor flat and confirm magnitude reads
                        # close to 1.0 -- adjust this number if it's consistently off.
# ----------------------------------------------------------------------

_bus = None


def init_accelerometer(i2c_bus_number=1):
    """
    Call once at startup. The MMA7660FC boots in Standby mode and won't
    produce real readings until MODE is explicitly set to Active.
    """
    global _bus
    _bus = smbus2.SMBus(i2c_bus_number)
    _bus.write_byte_data(I2C_ADDRESS, MODE_REG, MODE_ACTIVE)
    time.sleep(0.01)  # small settle time right after waking up


def _read_axis(register, max_retries=5):
    """
    Reads one axis. This chip has a real, documented quirk: if you catch
    it mid-internal-update, the ALERT bit gets set on that byte, meaning
    the value may be torn/invalid. The datasheet's own recommendation is
    simply to read again when that happens -- which is what this does.
    """
    raw = _bus.read_byte_data(I2C_ADDRESS, register)
    retries = 0
    while (raw & ALERT_BIT) and retries < max_retries:
        raw = _bus.read_byte_data(I2C_ADDRESS, register)
        retries += 1

    value = raw & VALUE_MASK
    if value & SIGN_BIT:
        value -= 64  # 6-bit two's complement: 32-63 actually mean -32 to -1
    return value


def read_accelerometer():
    """
    Returns (x, y, z) in g -- same units and shape everything in
    fall_detector.py / streaming_fall_detector.py already expects.
    """
    raw_x = _read_axis(XOUT_REG)
    raw_y = _read_axis(YOUT_REG)
    raw_z = _read_axis(ZOUT_REG)
    return raw_x / ACCEL_SCALE, raw_y / ACCEL_SCALE, raw_z / ACCEL_SCALE


if __name__ == "__main__":
    # Quick standalone check -- run this file directly on the Pi once wired up.
    # At rest, magnitude (x^2+y^2+z^2 square-rooted) should read close to 1.0.
    init_accelerometer()
    print("Reading MMA7660FC -- Ctrl+C to stop")
    while True:
        x, y, z = read_accelerometer()
        print(f"x={x:6.3f}  y={y:6.3f}  z={z:6.3f}")
        time.sleep(0.2)
