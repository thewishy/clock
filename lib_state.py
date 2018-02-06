import time
from multiprocessing import Queue

def state(input_queue, output_queue, buzzer_queue, distance_queue):
  # states [Clear, Pre-Alarm, Alarm, Snooze]
  state = "Clear"
  while (True):
    #print "I'm a little teapot"
    while (not input_queue.empty()):
      print "Got input"
      input=input_queue.get()
    while (not distance_queue.empty()):
      print "Got distance output"
      distance_action=distance_queue.get()
    time.sleep(0.25)