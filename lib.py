from multiprocessing import Queue
import time
import datetime

def notify_if_changed(queue, oldvalue, newvalue):
  if (oldvalue != newvalue):
    #print "Values differ!"
    queue.put(newvalue)
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
  
def oldcode():
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  #second = now.second
  

  # big_segment.clear()
  # Set hours
  big_segment.set_digit(0, int(hour / 10))     # Tens
  big_segment.set_digit(1, hour % 10)          # Ones
  # Set minutes
  big_segment.set_digit(2, int(minute / 10))   # Tens
  big_segment.set_digit(3, minute % 10)        # Ones