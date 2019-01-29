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
    print "SONOS Api Call Success", URL, r.status_code, r.json()
  else:
    print "SONOS Api Call Fail", URL, r.status_code, r.json()
    raise ConnectionError("Received bad response", r.status_code, "JSON Message", r.json())

def check_playing():
  print "Checking"
  r = requests.get(cfg['sonos']['address']+cfg['sonos']['speaker']+'/state')
  print "Result", r.json()
  if (r.status_code == 200 and r.json()['playbackState'] == "PLAYING"):
    print "SONOS Check Success"
  else:
    print "SONOS Api Call Fail", URL, r.status_code, r.json()
    raise ConnectionError("Received bad response", r.status_code, "JSON Message", r.json())

def calc_volume(heatingstate, windowstate):
  if (datetime.datetime.now().hour >= 21 or datetime.datetime.now().hour < 5):
    # Late night, quiet as possible
    base = 4
  else:
    # Rest of the day, a little louder
    base = 7
  if (heatingstate==1):
    base += 5
  elif (windowstate==1):
    base += 3
  return str(base)
    
def sonos(queue, buzzer_queue, heating_queue):
  heatingstate = 0
  windowstate = 0
  while (True):
    while (not queue.empty()):
      action=queue.get()
      print "Sonos got action", action
      if (action == "Pre-Alarm" or action == "Radio"):
        try:
          buzzer_queue.put("alarm_stop")
          # Leave any speaker group
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/leave')
          # Set Volume
          call = cfg['sonos']['address']+cfg['sonos']['speaker']+'/volume/' + calc_volume(heatingstate, windowstate)
          make_rest_call(call)
          # Switch on Radio 4
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/favorite/BBC Radio 4')
          # Set sleep timer (In seconds)
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/sleep/5400')
          # Unmute
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/unmute')

        except:
          print "Well, that went wrong... But tis only a pre-alarm"

      if (action == "Stop"):
        try:
          buzzer_queue.put("alarm_stop")
          # Leave any speaker group
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/leave')
          # Pause
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/pause')

        except:
          print "Well, that went wrong... But tis only a stop"
          
      if (action == "Alarm"):
        try:
          # Leave any speaker group
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/leave')
          # Set Volume
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/volume/20')
          # Switch on Radio 4
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/favorite/Sailing By')
          # Set sleep timer (In seconds)
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/sleep/3600')
          # Unmute
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/unmute')
          # Repeat
          make_rest_call(cfg['sonos']['address']+cfg['sonos']['speaker']+'/repeat/on')         
          for x in range(0, 15):
            if (not queue.empty()):
              break
            time.sleep(1)
            if (x==14):
              check_playing()
        except:
          print "Well, that went wrong... ACTIVATING THE CLAXON!"
          buzzer_queue.put("alarm_start")
    while (not heating_queue.empty()):
      try:
        newstate = heating_queue.get()
        print "Got info from automation system: ", newstate
        if (newstate<2):
          heatingstate = newstate
        else:
          newstate = newstate - 2
          print "Window State: ", newstate
          windowstate=newstate
        call = cfg['sonos']['address']+cfg['sonos']['speaker']+'/volume/' + calc_volume(heatingstate, windowstate)
        make_rest_call(call)
      except:
        print "Heating queue processing failed"
    time.sleep(0.5)
