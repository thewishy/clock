import requests
import time
import datetime

from multiprocessing import Process, Queue

from cfgmgr import get_config
cfg = get_config()


def light_wake():
  headers = { 'Authorization': cfg['light']['token'] }
  content = {"entity_id":cfg['light']['entity'],"transition":"300","brightness":"256","kelvin":"4000"}
  requests.post(cfg['light']['address']+"/api/services/light/turn_on", json=content, headers=headers)
  
def light_off():
  headers = { 'Authorization': cfg['light']['token'] }

  content = {"entity_id":"light.tradfri_bulb_e14_ws_opal_400lm"}
  requests.post(cfg['light']['address']+"/api/services/light/turn_off", json=content, headers=headers)

def light_on():
  headers = { 'Authorization': cfg['light']['token'] }
  if (datetime.datetime.now().hour >= 17 or datetime.datetime.now().hour < 6):
    #Night setting
    content = {"entity_id":cfg['light']['entity'],"transition":"5","brightness":"128","kelvin":"2700"}
  else:
    #Day Setting
    content = {"entity_id":cfg['light']['entity'],"transition":"5","brightness":"256","kelvin":"4000"}
    
  requests.post(cfg['light']['address']+"/api/services/light/turn_on", json=content, headers=headers)
  
def check_state():
  headers = { 'Authorization': cfg['light']['token'] }
  r = requests.get(cfg['light']['address']+'/api/states/'+cfg['light']['entity'], headers=headers)
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
        #try:
          if check_state():
            print "Turning off light"
            light_off()
          else:
            print "Turning on the light"
            light_on()
        #except:
          #print "That went wrong"
          
    time.sleep(0.5)
