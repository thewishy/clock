from tsl2561 import TSL2561 
import time
import requests
import paho.mqtt.client as mqtt
from cfgmgr import get_config
cfg = get_config()

def check_brightness(queue,notify_queue):
  tsl = TSL2561(debug=1)
  brightness = 0
  lux = 0

  while(True):
    try:
      lux = tsl.lux()
    except:
      print "Error polling Lux Sensor"
    #print lux 

    if brightness == 0:
      if (lux > 10):
        brightness = eval_brightness(queue,notify_queue,brightness,lux)
    elif brightness == 4:
      if (lux > 35 or lux <5):
        brightness = eval_brightness(queue,notify_queue,brightness,lux)
    elif brightness == 7:
      if (lux > 110 or lux < 25):
        brightness = eval_brightness(queue,notify_queue,brightness,lux)
    elif brightness == 15:
      if (lux < 90):
        brightness = eval_brightness(queue,notify_queue,brightness,lux)
    
    time.sleep(1)

def eval_brightness(queue,notify_queue,brightness,lux):
  if lux < 5:
    #print "Brightness Zero!"
    brightness = notify_change(queue,notify_queue,0)
  elif lux <30:
    brightness = notify_change(queue,notify_queue,4)
  elif lux > 100:
    brightness  = notify_change(queue,notify_queue,15)
  else:
    brightness = notify_change(queue,notify_queue,7)
  return brightness

def notify_change(queue, notify_queue,value):
  queue.put(value)
  if (cfg['lux']['role'] == "primary"):
    notify_queue.put("Lux:"+str(value))
  return value
