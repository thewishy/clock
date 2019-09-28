import time
from lib import notify_if_changed
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module



from cfgmgr import get_config
cfg = get_config()

def green_button_callback(channel):
  print("Green button was pushed!")
  buzzer_queue.put("beep_twice")
  queue.put("Double")


def set_buttons(queue):
  GPIO.setwarnings(False)    # Ignore warning for now
  GPIO.setmode(GPIO.BCM)     # Use physical pin numbering
  
  # Initate buttons (Off by default)
  GPIO.setup(int(cfg['buttons']['yellow_led']), GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(int(cfg['buttons']['green_led']), GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(int(cfg['buttons']['white_led']), GPIO.OUT, initial=GPIO.LOW)
  
  # Configure white led with static PWM
  #white_pwm = GPIO.PWM(int(cfg['buttons']['white_led']), 100)
  #white_pwm.start(20)

  # Set default state
  state="off"
  
  while (True):
    while (not queue.empty()):
     state=queue.get()
     print state
    if (state=="on"):
      GPIO.output(int(cfg['buttons']['yellow_led']), GPIO.HIGH)
      GPIO.output(int(cfg['buttons']['green_led']), GPIO.HIGH)
    else:
      GPIO.output(int(cfg['buttons']['yellow_led']), GPIO.LOW)
      GPIO.output(int(cfg['buttons']['green_led']), GPIO.LOW)
    time.sleep(1)
  
