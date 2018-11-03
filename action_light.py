import requests
import time
import datetime

from multiprocessing import Process, Queue



def make_call():
  headers = { 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhNWYyMzQxMjYwZDU0NTYxOTgyM2M3NGNmZjdmZGVlOSIsImlhdCI6MTU0MDMyNDk3MywiZXhwIjoxODU1Njg0OTczfQ.HM7GefyW-KZ1ut3gNx0hIsmwVVh8RfI6U_snqGc_yas" }

  content = {"entity_id":"scene.steve_wakeup"}
  requests.post("http://192.168.1.15:8123/api/services/scene/turn_on", json=content, headers=headers)

  
  
def make_ha_call(URL):
  r = requests.get(URL)

  
  if (r.status_code == 200 and r.json()['status'] == "success"):
    print "SONOS Api Call Success", URL, r.status_code, r.json()
  else:
    print "SONOS Api Call Fail", URL, r.status_code, r.json()
    raise ConnectionError("Received bad response", r.status_code, "JSON Message", r.json())


def light(queue):
  while (True):
    while (not queue.empty()):
      action=queue.get()
      print "Light got action", action
      if (action == "Pre-Alarm"):
        try:
          #
          make_call()

        except:
          print "Well, lighting went wrong!"

      if (action == "Stop"):
        try:
          print "Function not implemented"
        except:
          print "Well, light went wrong on stop"
          
    time.sleep(1)
