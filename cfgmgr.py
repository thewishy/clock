import json

def get_config():
  #print "Getting Config"
  with open("/root/clock.json",'r') as jsonfile:
    cfg = json.load(jsonfile)
  #print cfg
  return cfg