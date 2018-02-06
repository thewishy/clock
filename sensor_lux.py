from lib import notify_if_changed
from tsl2561 import TSL2561 
import time

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
      brightness = notify_if_changed(queue,brightness,0)
    elif lux <30:
      brightness = notify_if_changed(queue,brightness,4)
    elif lux > 100:
      brightness  = notify_if_changed(queue,brightness,15)
    else:
      brightness = notify_if_changed(queue,brightness,7)
    time.sleep(1)