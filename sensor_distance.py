import smbus
import struct
import time
from lib import notify_if_changed

from cfgmgr import get_config
cfg = get_config()
alarmthreshold = int(cfg['distance']['alarmthreshold'])
lightthreshold = int(cfg['distance']['lightthreshold'])

def bswap(val):
    return struct.unpack('<H', struct.pack('>H', val))[0]
def mread_word_data(adr, reg):
    return bswap(bus.read_word_data(adr, reg))
def mwrite_word_data(adr, reg, data):
    return bus.write_word_data(adr, reg, bswap(data))
def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)
def VL53L0X_decode_vcsel_period(vcsel_period_reg):
# Converts the encoded VCSEL period register value into the real
# period in PLL clocks
    vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
    return vcsel_period_pclks;


def check_distance(queue, buzzer_queue, light_queue):
  VL53L0X_REG_IDENTIFICATION_MODEL_ID		= 0x00c0
  VL53L0X_REG_IDENTIFICATION_REVISION_ID		= 0x00c2
  VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD	= 0x0050
  VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD	= 0x0070
  VL53L0X_REG_SYSRANGE_START			= 0x000

  VL53L0X_REG_RESULT_INTERRUPT_STATUS 		= 0x0013
  VL53L0X_REG_RESULT_RANGE_STATUS 		= 0x0014

  address = 0x29

  bus = smbus.SMBus(1)
  
  last_triggered = 0
  last_cleared = 0

  #val1 = bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_REVISION_ID)
  #print "Revision ID: " + hex(val1)
  #val1 = bus.read_byte_data(address, VL53L0X_REG_IDENTIFICATION_MODEL_ID)
  #print "Device ID: " + hex(val1)
  #	case VL53L0X_VCSEL_PERIOD_PRE_RANGE:
  #		Status = VL53L0X_RdByte(Dev,
  #			VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD,
  #			&vcsel_period_reg);
  #val1 = bus.read_byte_data(address, VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)
  #print "PRE_RANGE_CONFIG_VCSEL_PERIOD=" + hex(val1) + " decode: " + str(VL53L0X_decode_vcsel_period(val1))


  #	case VL53L0X_VCSEL_PERIOD_FINAL_RANGE:
  #		Status = VL53L0X_RdByte(Dev,
  #			VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD,
  #			&vcsel_period_reg);

  #val1 = bus.read_byte_data(address, VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)
  #print "FINAL_RANGE_CONFIG_VCSEL_PERIOD=" + hex(val1) + " decode: " + str(VL53L0X_decode_vcsel_period(val1))

  while (True):
    #		Status = VL53L0X_WrByte(Dev, VL53L0X_REG_SYSRANGE_START, 0x01);
    val1 = bus.write_byte_data(address, VL53L0X_REG_SYSRANGE_START, 0x01)

    #		Status = VL53L0X_RdByte(Dev, VL53L0X_REG_RESULT_RANGE_STATUS,
    #			&SysRangeStatusRegister);
    #		if (Status == VL53L0X_ERROR_NONE) {
    #			if (SysRangeStatusRegister & 0x01)
    #				*pMeasurementDataReady = 1;
    #			else
    #				*pMeasurementDataReady = 0;
    #		}

    cnt = 0
    while (cnt < 100): # 1 second waiting time max
      time.sleep(0.010)
      val = bus.read_byte_data(address, VL53L0X_REG_RESULT_RANGE_STATUS)
      if (val & 0x01):
        break
      cnt += 1

    if (val & 0x01):
      data = bus.read_i2c_block_data(address, 0x14, 12)
      DeviceRangeStatusInternal = ((data[0] & 0x78) >> 3)
      if (DeviceRangeStatusInternal == 11):
        #	Status = VL53L0X_ReadMulti(Dev, 0x14, localBuffer, 12);
        
        #print data
        #print "ambient count " + str(makeuint16(data[7], data[6]))
        #print "signal count " + str(makeuint16(data[9], data[8]))
        #		tmpuint16 = VL53L0X_MAKEUINT16(localBuffer[11], localBuffer[10]);
        distance = makeuint16(data[11], data[10])
        if (distance < alarmthreshold):
          print "Triggered ", distance
          # See if someone has removed hand from sensor and then put it back
          if last_triggered < last_cleared:
            # Was the trigger / untrigger in the last 3 seconds
            if last_triggered > time.time()-3:
              #Second triggering
              print "Second Trigger"
              buzzer_queue.put("beep_twice")
              queue.put("Double")
              last_triggered = time.time()
              # Twice should be about the max we want. Leave a little time for the hand to be moved
              time.sleep(1)
            else:
              # First triggering
              print "First Trigger"
              buzzer_queue.put("beep_once")
              queue.put("Triggered")
              last_triggered = time.time()
              print last_triggered
              print time.time()
          #Sensor is being held
          elif last_triggered+1 < time.time():

            print "Retrigger"
            buzzer_queue.put("beep_once")
            queue.put("Triggered")
            last_triggered = time.time()  
          else:
            print "Skip"
        elif (distance<lightthreshold):
          print "Distance Sensor: Turn on the light!"
          light_queue.put("Toggle")
          # As there is no feedback, and we need to wait for the turnon command to take affect, suspend distance processing for a few seconds
          time.sleep(3)
        else:
          last_cleared = time.time()
        
        # If read was good, wait half a second then get another read
        time.sleep(0.5)
        #print "Bad read, Code ", DeviceRangeStatusInternal, "Distance reported", str(makeuint16(data[11], data[10]))

 
  