import time
from lib import notify_if_changed
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module



from cfgmgr import get_config
cfg = get_config()

def yellow_button_callback(channel):
  time.sleep(0.1)
  if (GPIO.input(int(cfg['buttons']['yellow_button'])) != GPIO.HIGH):
    print("Noise Detected Yellow Channel")
  else:
    print("Yellow button was pushed!")
    buzzer_queue.put("beep_once")
    queue.put("Triggered")

def green_button_callback(channel):
  time.sleep(0.1)
  if (GPIO.input(int(cfg['buttons']['green_button'])) != GPIO.HIGH):
    print("Noise Detected Green Channel")
  else:
    print("Green button was pushed!")
    buzzer_queue.put("beep_twice")
    queue.put("Double")
  
def white_button_callback(channel):
  time.sleep(0.1)
  if (GPIO.input(int(cfg['buttons']['white_button'])) != GPIO.HIGH):
    print("Noise Detected White Channel")
  else:
    print("White button was pushed!")
    light_queue.put("Toggle")

def blue_button_callback(channel):
  time.sleep(0.1)
  if (GPIO.input(int(cfg['buttons']['blue_button'])) != GPIO.HIGH):
    print("Noise Detected Blue Channel")
  else:
    print("Blue button was pushed!")
    sonos_queue.put("Say_Time")

def check_buttons(local_queue, local_buzzer_queue, local_light_queue, local_sonos_queue):
  global queue
  queue = local_queue
  global buzzer_queue
  buzzer_queue = local_buzzer_queue
  global light_queue
  light_queue = local_light_queue
  global sonos_queue
  sonos_queue = local_sonos_queue
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

  if 'blue_button' in cfg['buttons']:
    GPIO.setup(int(cfg['buttons']['blue_button']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(int(cfg['buttons']['blue_button']),GPIO.RISING,callback=blue_button_callback,bouncetime=500) 
  while (True):
    time.sleep(100)
