import time
import datetime
import os

def dt_parse(t):
    # Example: 2017-09-30 08:30:00
    if (t is not None and t != "None"):
      return datetime.datetime.strptime(t[0:19],'%Y-%m-%d %H:%M:%S')
    else:
      return None

def read_from_backup():
  try:
    f = open('nextalarm.txt', 'r')
    datafromfile = f.readline()
    f.close()
    return datafromfile
  except:
    print "File handling error"

def write_to_backup(value):
  try:
    f = open('nextalarm.txt', 'w')
    f.write(value)
    f.close()
  except:
    print "File handling error"