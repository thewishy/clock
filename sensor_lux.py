from tsl2561 import TSL2561 
import time
import requests
from cfgmgr import get_config
cfg = get_config()

def check_brightness(queue):
  tsl = TSL2561(debug=1)
  brightness = 0
  lux = 0
  while(True):
    try:
      lux = tsl.lux()
    except:
      print "Error polling Lux Sensor"
    #print lux 
    if lux < 5:
      #print "Brightness Zero!"
      brightness = check_change(queue,brightness,0)
    elif lux <30:
      brightness = check_change(queue,brightness,4)
    elif lux > 100:
      brightness  = check_change(queue,brightness,15)
    else:
      brightness = check_change(queue,brightness,7)
    time.sleep(1)
    
def check_change(queue, oldvalue, newvalue):
  if (oldvalue != newvalue):
    #print "Values differ!"
    queue.put(newvalue)
    if (cfg['lux']['notify_other']):
      print "Brightness: Making REST Call"
      try:
        r = requests.get(cfg['lux']['address']+str(newvalue))
      except Exception as err:
        print("HTTP Error making Lux rest call", err)
  return newvalue