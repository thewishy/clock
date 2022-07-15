from tsl2561 import TSL2561 
import time
import paho.mqtt.client as mqtt
from cfgmgr import get_config
cfg = get_config()

def mqtt_start(publishing_queue_local,lux_queue_local,light_status_queue_local):
  global publishing_queue
  global lux_queue
  global light_status_queue
  global mqtt_client
  publishing_queue = publishing_queue_local
  lux_queue = lux_queue_local
  light_status_queue = light_status_queue_local

  
  mqtt_client = mqtt.Client(client_id=cfg['core']['name']+"_sensor_mqtt")
  mqtt_client.on_connect = on_mqtt_connect
  
  mqtt_client.connect(cfg['mqtt']['server'], 1883, 60)
  mqtt_client.on_message = on_mqtt_message
  while(True):
    mqtt_client.loop()
    while(not publishing_queue.empty()):
      action=publishing_queue.get()
      # print action
      if(action.split(":")[0]=="Lux"):
        # print "Pushing Lux value to MQTT"
        mqtt_client.publish(cfg['lux']['topic'],action.split(":")[1])
      else:
        print "Unhandled Action"

def on_mqtt_connect(client, userdata, flags, rc):
  #print("Subscribed")
  mqtt_client.subscribe(cfg['light']['topic'])
  if (cfg['lux']['role'] == "secondary"):
    mqtt_client.subscribe(cfg['lux']['topic'])

def on_mqtt_message(mqtt_client, userdata, message):
  # print message.topic
  if (message.topic == cfg['light']['topic']):
    if (message.payload.decode("utf-8")=="on"):
      light_status_queue.put(1)
    else:
      light_status_queue.put(0)
  elif (message.topic == cfg['lux']['topic']):
    lux = int(message.payload.decode("utf-8"))
    # print lux
    lux_queue.put(lux)

def on_queue_message(mqtt_client):
  try:
    mqtt_client.publish(cfg['lux']['topic'],value)
  except Exception as err:
    print("MQTT Error publishing lux", err)