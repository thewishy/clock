import requests
import time
import datetime

from multiprocessing import Process, Queue

from cfgmgr import get_config
cfg = get_config()


def coffee_on():
  headers = { 'Authorization': cfg['homeassistant']['token'] }
  content = {"entity_id":cfg['coffee']['entity']}
    
  requests.post(cfg['homeassistant']['address']+"/api/services/switch/turn_on", json=content, headers=headers)

def coffee(queue):
  while (True):
    while (not queue.empty()):
      action=queue.get()
      print "Coffee got action", action
      if (action == "Make"):
        try:
          if (datetime.datetime.now().hour >= 4 and datetime.datetime.now().hour < 11):
            coffee_on()
          else:
            print "Coffee request out of time range"
        except:
          print "Well, coffee went wrong!"
          
    time.sleep(30)
