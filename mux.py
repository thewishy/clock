import smbus
import time

def i2c_mux_setup(i2c_channel_setup):
  I2C_address = 0x70
  I2C_bus_number = 1
  bus = smbus.SMBus(I2C_bus_number)
  bus.write_byte(I2C_address,i2c_channel_setup)
  time.sleep(0.1)
  print "TCA9548A I2C channel status:", bin(bus.read_byte(I2C_address))
