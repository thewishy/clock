import requests
import time
import datetime

from multiprocessing import Process, Queue

from cfgmgr import get_config
cfg = get_config()



def light_wake():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  content = {"entity_id":cfg['light']['entity'],"transition":"300","brightness":"256","kelvin":"4000"}
  requests.post(cfg['homeassistant']['address']+"/api/services/light/turn_on", json=content, headers=headers)

def light_low():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  content = {"entity_id":cfg['light']['entity'],"transition":"5","brightness":"128","kelvin":"2700"}
  requests.post(cfg['homeassistant']['address']+"/api/services/light/turn_on", json=content, headers=headers)
  
def light_off():
  headers = { 'Authorization': cfg['homeassistant']['token'] }

  content = {"entity_id":cfg['light']['entity']}
  requests.post(cfg['homeassistant']['address']+"/api/services/light/turn_off", json=content, headers=headers)

def light_on():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  if (datetime.datetime.now().hour >= 17 or datetime.datetime.now().hour < 6):
    #Night setting
    content = {"entity_id":cfg['light']['entity'],"transition":"5","brightness":"128","kelvin":"2700"}
  else:
    #Day Setting
    content = {"entity_id":cfg['light']['entity'],"transition":"5","brightness":"256","kelvin":"4000"}
  requests.post(cfg['homeassistant']['address']+"/api/services/light/turn_on", json=content, headers=headers)
  
def check_state():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  r = requests.get(cfg['homeassistant']['address']+'/api/states/'+cfg['light']['entity'], headers=headers)
  print "Light state", r.json()
  if (r.json()['state']=="off"):
    return False
  else:
    return True
  

def light(queue):
  wait_until = None
  while (True):
    if (wait_until is not None and wait_until < time.time()):
      print "Switching off light due to time delay"
      wait_until = None
      light_off()
    while (not queue.empty()):
      action=queue.get()
      print "Light got action", action
      if (action == "Pre-Alarm"):
        try:
          light_wake()
        except:
          print "Well, lighting went wrong!"
          
      if (action == "Toggle"):
        if check_state():
          print "Turning off light"
          light_off()
        else:
          print "Turning on the light"
          light_on()

      if (action == "On"):
        light_on()
          
      if (action == "Off"):
        light_off()
        
      if (action == "Off-Delay"):
        print "Setting time delay"
        wait_until = time.time() + int(cfg['light']['delay'])
        light_low()
        
    time.sleep(0.5)
