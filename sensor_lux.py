from tsl2561 import TSL2561 
import time
import requests
import paho.mqtt.client as mqtt
from cfgmgr import get_config
cfg = get_config()
#mqtt_client = None

def check_brightness(local_queue):
  global queue
  global mqtt_client
  queue = local_queue
  if (cfg['lux']['role'] == "primary" or cfg['lux']['role'] == "standalone"):
    tsl = TSL2561(debug=1)
    brightness = 0
    lux = 0
    if (cfg['lux']['role'] == "primary"):
      mqtt_client = mqtt.Client()
      #mqtt_client.on_connect = on_connect
      
      mqtt_client.connect(cfg['lux']['mqtt_server'], 1883, 60)
      #mqtt_client.subscribe(cfg['lux']['topic'])
      #mqtt_client.on_message = on_mqtt_message
    while(True):
      try:
        lux = tsl.lux()
      except:
        print "Error polling Lux Sensor"
      #print lux 

      if brightness == 0:
        if (lux > 10):
          brightness = eval_brightness(queue,brightness,lux)
      elif brightness == 4:
        if (lux > 35 or lux <5):
          brightness = eval_brightness(queue,brightness,lux)
      elif brightness == 7:
        if (lux > 110 or lux < 25):
          brightness = eval_brightness(queue,brightness,lux)
      elif brightness == 15:
        if (lux < 90):
          brightness = eval_brightness(queue,brightness,lux)
      time.sleep(1)
  elif (cfg['lux']['role'] == "secondary"):
    print "Acting as secondary"
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_mqtt_connect
    
    mqtt_client.connect(cfg['lux']['mqtt_server'], 1883, 60)
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.loop_forever()

def on_mqtt_connect(client, userdata, flags, rc):
  print("Subscribed")
  mqtt_client.subscribe(cfg['lux']['topic'])

def on_mqtt_message(mqtt_client, userdata, message):
  lux = int(message.payload.decode("utf-8"))
  print lux
  queue.put(lux)

def eval_brightness(queue, brightness,lux):
  if lux < 5:
    #print "Brightness Zero!"
    brightness = notify_change(queue,0)
  elif lux <30:
    brightness = notify_change(queue,4)
  elif lux > 100:
    brightness  = notify_change(queue,15)
  else:
    brightness = notify_change(queue,7)
  return brightness

def notify_change(queue, value):
  queue.put(value)
  if (cfg['lux']['role'] == "primary"):
    try:
      mqtt_client.publish(cfg['lux']['topic'],value)
    except Exception as err:
      print("MQTT Error publishing lux", err)
  return value
