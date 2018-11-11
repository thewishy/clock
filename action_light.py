import requests
import time
import datetime

from multiprocessing import Process, Queue



def light_wake():
  headers = { 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhNWYyMzQxMjYwZDU0NTYxOTgyM2M3NGNmZjdmZGVlOSIsImlhdCI6MTU0MDMyNDk3MywiZXhwIjoxODU1Njg0OTczfQ.HM7GefyW-KZ1ut3gNx0hIsmwVVh8RfI6U_snqGc_yas" }

  content = {"entity_id":"scene.steve_wakeup"}
  requests.post("http://192.168.1.15:8123/api/services/scene/turn_on", json=content, headers=headers)

def light_off():
  headers = { 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhNWYyMzQxMjYwZDU0NTYxOTgyM2M3NGNmZjdmZGVlOSIsImlhdCI6MTU0MDMyNDk3MywiZXhwIjoxODU1Njg0OTczfQ.HM7GefyW-KZ1ut3gNx0hIsmwVVh8RfI6U_snqGc_yas" }

  content = {"entity_id":"light.tradfri_bulb_e14_ws_opal_400lm"}
  requests.post("http://192.168.1.15:8123/api/services/light/turn_off", json=content, headers=headers)

def light_on():
  headers = { 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhNWYyMzQxMjYwZDU0NTYxOTgyM2M3NGNmZjdmZGVlOSIsImlhdCI6MTU0MDMyNDk3MywiZXhwIjoxODU1Njg0OTczfQ.HM7GefyW-KZ1ut3gNx0hIsmwVVh8RfI6U_snqGc_yas" }
  if (datetime.datetime.now().hour >= 17 or datetime.datetime.now().hour < 6):
    #Night setting
    content = {"entity_id":"light.tradfri_bulb_e14_ws_opal_400lm","transition":"5","brightness":"128","kelvin":"2700"}
  else:
    #Day Setting
    content = {"entity_id":"light.tradfri_bulb_e14_ws_opal_400lm","transition":"5","brightness":"256","kelvin":"4000"}
    
  requests.post("http://192.168.1.15:8123/api/services/light/turn_on", json=content, headers=headers)
  
def check_state():
  headers = { 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhNWYyMzQxMjYwZDU0NTYxOTgyM2M3NGNmZjdmZGVlOSIsImlhdCI6MTU0MDMyNDk3MywiZXhwIjoxODU1Njg0OTczfQ.HM7GefyW-KZ1ut3gNx0hIsmwVVh8RfI6U_snqGc_yas" }
  r = requests.get('http://192.168.1.15:8123/api/states/light.tradfri_bulb_e14_ws_opal_400lm', headers=headers)
  print "Light state", r.json()
  if (r.json()['state']=="off"):
    return False
  else:
    return True
  

def light(queue):
  while (True):
    while (not queue.empty()):
      action=queue.get()
      print "Light got action", action
      if (action == "Pre-Alarm"):
        try:
          light_wake()
        except:
          print "Well, lighting went wrong!"
          
      if (action == "Toggle"):
        try:
          if check_state():
            print "Turning off light"
            light_off()
          else:
            print "Turning on the light"
            light_on()
        except:
          print "That went wrong"
          
    time.sleep(0.5)
