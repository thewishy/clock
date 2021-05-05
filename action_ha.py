import requests
import time
import datetime

from multiprocessing import Process, Queue

from cfgmgr import get_config
cfg = get_config()

class ConnectionError(Exception):
  pass

def make_rest_call(URL):
  r = requests.get(URL)
  
  if (r.status_code == 200 and r.json()['status'] == "success"):
    print "Home Assistant Api Call Success", URL, r.status_code, r.json()
  else:
    print "Home Assistant Api Call Fail", URL, r.status_code, r.json()
    raise ConnectionError("Received bad response", r.status_code, "JSON Message", r.json())

def check_playing():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  r = requests.get(cfg['homeassistant']['address']+'/api/states/media_player.bedroom', headers=headers)
  if (r.status_code == 200 and r.json()['state'] == "playing"):
    print "Home Assistant Check Success"
  else:
    print "Home Assistant Api Call Fail", URL, r.status_code, r.json()
    raise ConnectionError("Received bad response", r.status_code, "JSON Message", r.json())
    
def ha(queue, buzzer_queue):
  while (True):
    while (not queue.empty()):
      action=queue.get()
      print "Home Assistant got action", action
      if (action == "Pre-Alarm" or action == "Radio"):
        try:
          buzzer_queue.put("alarm_stop")
          headers = { 'Authorization': cfg['homeassistant']['token'] }
          content = {}
          requests.post(cfg['homeassistant']['address']+"/api/services/script/bedroom_radio_4_for_1hr", json=content, headers=headers)
        except:
          print "Well, that went wrong... But tis only a pre-alarm / radio request"

      if (action == "Say_Time"):
        try:
          headers = { 'Authorization': cfg['homeassistant']['token'] }
          content = {}
          requests.post(cfg['homeassistant']['address']+"/api/services/script/bedroom_say_time", json=content, headers=headers)
        except:
          print "Well, that went wrong... But tis only a time request"

      if (action == "Stop"):
        try:
          print "Alarm / Media Stopping"
          buzzer_queue.put("alarm_stop")
          headers = { 'Authorization': cfg['homeassistant']['token'] }
          content = {"entity_id:media_player.bedroom"}
          requests.post(cfg['homeassistant']['address']+"/api/services/media_player/media_stop", json=content, headers=headers)
        except:
          print "Well, that went wrong... But tis only a stop"

      if (action == "Wakeup"):
        try:
          print "Calling Wakeup Script"
          headers = { 'Authorization': cfg['homeassistant']['token'] }
          content = {}
          requests.post(cfg['homeassistant']['address']+"/api/services/script/"+cfg['wakeup']['script'], json=content, headers=headers)
        except:
          print "Well, that went wrong... But tis only a wakeup script"

      if (action == "Alarm"):
        try:
          headers = { 'Authorization': cfg['homeassistant']['token'] }
          content = {}
          requests.post(cfg['homeassistant']['address']+"/api/services/script/bedroom_radio_alarm", json=content, headers=headers)       
          # Check that the Sonos actually activated
          for x in range(0, 15):
            if (not queue.empty()):
              break
            time.sleep(1)
            if (x==14):
              check_playing()
        except:
          print "Well, that went wrong... ACTIVATING THE CLAXON!"
          buzzer_queue.put("alarm_start")
    time.sleep(0.5)
