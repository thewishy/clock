import RPi.GPIO as GPIO
import time
from multiprocessing import Queue




def buzzer(queue):
  ''' Consumer of messages to run alarm buzzer via Queue
  Acceptable messages
  beep_once - Single short Beep
  beep_twice - Two short beeps
  
  alarm_start - Continuous alarm clock alarm
  alarm_stop - Cancel continous alarm clock alarm
  
  Beep instructions are considered a "priority" over alarm
  '''
  
  alarm = False
  beeps = 0
  
  #GPIO Setup
  buzzer_pin = 21
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buzzer_pin, GPIO.IN)
  GPIO.setup(buzzer_pin, GPIO.OUT)
  while (True):
  
    while (not queue.empty()):
      action=queue.get()
      print "Buzzproc Got message", action
      if action == 'beep_once':
        beeps += 1
      elif action == 'beep_twice':
        beeps += 2
      elif action == 'beep_thrice':
        beeps += 3
      elif action == 'alarm_start':
        alarm=True
      else:
        alarm=False
      
    if beeps > 0:
      while (beeps > 0):
        GPIO.output(buzzer_pin, True)
        time.sleep(0.1)
        GPIO.output(buzzer_pin, False)
        beeps -= 1
        time.sleep(0.15)
    elif alarm:
      print "Alarm"
      GPIO.output(buzzer_pin, True)
      time.sleep(0.3)
      GPIO.output(buzzer_pin, False)
      time.sleep(1)
        
    time.sleep(0.1)

    
    
def alarm(duration=0.5,pause=0.5,repeat=0):
  #GPIO.setwarnings(False) # Less of a problem if you run the cleanup routine!
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buzzer_pin, GPIO.IN)
  GPIO.setup(buzzer_pin, GPIO.OUT)
  
  for x in range(0, repeat):
    print "Beep!"
    #GPIO.output(buzzer_pin, True)
    time.sleep(duration)                          # beeps for 1 second
    #GPIO.output(buzzer_pin, False)
    time.sleep(pause)                          # silence for 1 second
  GPIO.cleanup(buzzer_pin)
  

#alarm(duration=0.01,pause=0.5,repeat=2)