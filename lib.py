from multiprocessing import Queue
import time
import datetime

def notify_if_changed(queue, oldvalue, newvalue, prepend=None):
  if (oldvalue != newvalue):
    #print "Values differ!"
    if (prepend==None):
      queue.put(newvalue)
    else:
      queue.put(prepend+newvalue)
  return newvalue

def display_text(inputdatetime):
  #if (inputdatetime is None):
  #  return "----"
  hour = inputdatetime.hour
  minute = inputdatetime.minute
  return str(hour / 10)+str(hour % 10)+str(minute / 10)+str(minute % 10)

def display_text_seconds(delta):
  minute=delta/60
  second = delta%60
  if (delta<=599):
    return "-"+str(minute % 10)+str(second / 10)+str(second % 10)
  else:
    return str(minute / 10)+str(minute % 10)+str(second / 10)+str(second % 10)
