import time
from lib import notify_if_changed
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module



from cfgmgr import get_config
cfg = get_config()

def yellow_button_callback(channel):
  print("Yellow button was pushed!")
  buzzer_queue.put("beep_once")
  queue.put("Triggered")

def green_button_callback(channel):
  print("Green button was pushed!")
  buzzer_queue.put("beep_twice")
  queue.put("Double")
  
def white_button_callback(channel):
  print("White button was pushed!")
  light_queue.put("Toggle")
  
def check_buttons(local_queue, local_buzzer_queue, local_light_queue):
  global queue
  queue = local_queue
  global buzzer_queue
  buzzer_queue = local_buzzer_queue
  global light_queue
  light_queue = local_light_queue
  GPIO.setwarnings(False)    # Ignore warning for now
  GPIO.setmode(GPIO.BCM)     # Use physical pin numbering
  
  # Setup Yellow button
  GPIO.setup(int(cfg['buttons']['yellow_button']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(int(cfg['buttons']['yellow_button']),GPIO.RISING,callback=yellow_button_callback,bouncetime=500) 

  # Setup Green button
  GPIO.setup(int(cfg['buttons']['green_button']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(int(cfg['buttons']['green_button']),GPIO.RISING,callback=green_button_callback,bouncetime=500) 
  
  # Setup White button
  GPIO.setup(int(cfg['buttons']['white_button']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(int(cfg['buttons']['white_button']),GPIO.RISING,callback=white_button_callback,bouncetime=500) 
  
  while (True):
    time.sleep(100)