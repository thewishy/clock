import RPi.GPIO as GPIO
import time
from multiprocessing import Queue
buzzer_pin = 21
#GPIO.setwarnings(False) # Less of a problem if you run the cleanup routine!
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)
  
for x in range(0, 100):
  print "Beep!"
  GPIO.output(buzzer_pin, True)
  time.sleep(1)                          # beeps for 1 second
  GPIO.output(buzzer_pin, False)
  time.sleep(1)                          # silence for 1 second

GPIO.cleanup(buzzer_pin)
  

#alarm(duration=0.01,pause=0.5,repeat=2)