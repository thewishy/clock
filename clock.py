#!/usr/bin/python

import time
import datetime

from multiprocessing import Process, Queue
from Adafruit_LED_Backpack import SevenSegment

# Project Modules
from cfgmgr import get_config
cfg = get_config()

import mux
import sensor_lux
import sensor_ntp
import sensor_distance
import action_buzz
import input_gcal
import sensor_heating
import action_sonos
import action_light
import action_coffee
from lib import display_text
from lib import display_text_seconds


### INIT WORK ###

process_check = time.time()+60

if (cfg['core']['mux']):
  #Setup I2C Multiplexer
  #I2C mux was added when I had problems with I2C comms on the 1.2" Adafruit 7 Segment
  #This problem wasn't really solved by the mux, running the IO at 5v sorted it though.. Anyway, it's wired in now...
  mux.i2c_mux_setup(0b00011111)



#Setup Lux Monitor process
lux_queue = Queue()
if (cfg['core']['lux']):
  lux_process = Process(target=sensor_lux.check_brightness, args=(lux_queue,))
  lux_process.daemon = True
  lux_process.start()
  print "-> Lux PID", lux_process.pid
brightness = 1

#Setup NTP Monitor process
ntp_queue = Queue()
ntp_process = Process(target=sensor_ntp.check_ntp, args=(ntp_queue,))
ntp_process.daemon = True
ntp_process.start()
print "-> NTP PID", ntp_process.pid
ntp_bad = 1

#Setup Google Cal process
gcal_queue = Queue()
gcal_process = Process(target=input_gcal.gcal, args=(gcal_queue,))
gcal_process.daemon = True
gcal_process.start()
next_alarm = None
print "-> gcal PID", gcal_process.pid

# Setup Buzzer
buzzer_queue = Queue()
buzzer_process = Process(target=action_buzz.buzzer, args=(buzzer_queue,))
buzzer_process.daemon = True
buzzer_process.start()
print "-> buzzer PID", buzzer_process.pid

#Setup Light Process
light_queue = Queue()
if (cfg['core']['light']):
  light_process = Process(target=action_light.light, args=(light_queue,))
  light_process.daemon = True
  light_process.start()
  print "-> light PID", light_process.pid

#Setup Light Process
coffee_queue = Queue()
if (cfg['core']['coffee']):
  coffee_process = Process(target=action_coffee.coffee, args=(coffee_queue,))
  coffee_process.daemon = True
  coffee_process.start()
  print "-> Coffee PID", coffee_process.pid
  print "****************************************************************************************************************************************"
  print "*** Coffee switch is ARMED. If you're reading this, perhaps you're testing? If so, did you switch the coffeee machine off manually?? ***"
  print "****************************************************************************************************************************************"
  
#Setup Distance Monitor process
distance_queue = Queue()
distance_process = Process(target=sensor_distance.check_distance, args=(distance_queue,buzzer_queue,light_queue))
distance_process.daemon = True
distance_process.start()
print "-> distance PID", distance_process.pid

#Setup heating HTTP Process
heating_queue = Queue()
if (cfg['core']['http']):
  heating_process = Process(target=sensor_heating.run, args=(heating_queue,))
  heating_process.daemon = True
  heating_process.start()
  print "-> heating PID", heating_process.pid

#Setup Sonos Process
sonos_queue = Queue()
sonos_process = Process(target=action_sonos.sonos, args=(sonos_queue,buzzer_queue, heating_queue))
sonos_process.daemon = True
sonos_process.start()
print "-> Sonos PID", sonos_process.pid

#Setup Status
# states [Clear, Pre-Alarm, Alarm, Snooze, No-Alarm]
state = "Clear"
warned = "No"
snooze_until = None

#Setup 7 Segment Displays
clock_segment = SevenSegment.SevenSegment(address=int(cfg['core']['clock_addr'],16))
alarm_segment = SevenSegment.SevenSegment(address=int(cfg['core']['alarm_addr'],16))

# Initialize the display. Must be called once before using the display.
clock_segment.begin()
alarm_segment.begin()

# Toggle colon
#segment.set_colon(second % 2)              # Toggle colon at 1Hz
clock_segment.set_colon(True) 

# Set Left Colon 
#clock_segment.set_left_colon(False)


print "Press CTRL+Z to exit"

#Quick test code
#coffee_queue.put("Make")

### BEGIN WORK ###
# Continually update the time on a 4 char, 7-segment display
while(True):
  
  while (not lux_queue.empty()):
    brightness=lux_queue.get()
  
  while (not ntp_queue.empty()):
    ntp_bad=ntp_queue.get()
    
  while ((state == "Clear" or state == "No-Alarm") and not gcal_queue.empty()):
    print "Alarm time message action", state
    test_alarm=gcal_queue.get()
    if (test_alarm is None):
      print "Alarm is none, which is OK"
      next_alarm = None
    elif (int(test_alarm.strftime('%s')) - int(datetime.datetime.now().strftime('%s')) >=0):
      print "Alarm is good"
      next_alarm=test_alarm
    else:
      print "Alarm is in the past, skipping"

  #while (not state_recieve.empty()):
  #  print "Main process setting state"
  #  state=state_recieve.get()
  #  print state

  while (not distance_queue.empty()):
      print "Got distance output"
      distance_action=distance_queue.get()
      print distance_action
      if (distance_action == "Double"):
        if (state == "Alarm"):
          print "Clearing Alarm"
          state = "Clear"
          # Expectation is that there is either a new time held in the gcal queue, or that it will send one soon...
          next_alarm = None
          snooze_until = None
          warned = "No"
          # Switch Sonos to Radio mode
          if (cfg['alarm']['switch_off_radio']):
            sonos_queue.put("Stop")
          else:
            sonos_queue.put("Radio")
          if (cfg['alarm']['switch_off_light']):
            light_queue.put("Off-Delay")
          coffee_queue.put("Make")
        elif (state=="Snooze" or state=="Pre-Alarm" or state=="Pre-Pre-Alarm"):
          print "Clearing Alarm"
          state = "Clear"
          next_alarm = None
          snooze_until = None   
          warned = "No"
          coffee_queue.put("Make")
          if (cfg['alarm']['switch_off_radio']):
            sonos_queue.put("Stop")
          if (cfg['alarm']['switch_off_light']):
            light_queue.put("Off-Delay")
        else:
          print "Hmm, that doesn't really mean anything to me"
      elif (distance_action == "Triggered"):
        if (state == "Alarm"):
          print "Snooze time"
          sonos_queue.put("Radio")
          state = "Snooze"
          warned = "No"
          snooze_until = datetime.datetime.now() + datetime.timedelta(minutes=5)
          print "Snoozing until: ", snooze_until       
        elif (state=="Snooze"):
          snooze_until = snooze_until + datetime.timedelta(minutes=5)
          warned = "No"
          print "More Snoozing until: ", snooze_until              
        elif (state=="Pre-Alarm"):
         state = "Snooze"
         snooze_until = next_alarm + datetime.timedelta(minutes=5)
         warned = "No"
        elif (state=="Pre-Pre-Alarm"):
         state = "Snooze"
         snooze_until = next_alarm + datetime.timedelta(minutes=5)
         warned = "No"
        else:
          print "So you want radio?"
          sonos_queue.put("Radio")
        
    
  
  
  # Now process some state
  # states [Clear, Pre-Pre-Alarm, Pre-Alarm, Alarm, Snooze, No-Alarm]
  # First thing - check if snoozing, clear snooze if required
  if (snooze_until is not None):
    snoozedelta = int(snooze_until.strftime('%s')) - int(datetime.datetime.now().strftime('%s'))
    if (snoozedelta <= 0):
      snooze_until = None
      state = "Alarm"
      sonos_queue.put("Alarm")
    elif (snoozedelta <= 60):
      print "SnoozeDelta should warn"
      if (warned == "No"):
        print "Warning"
        buzzer_queue.put("beep_once")
        warned = "Yes"
        print "Warned"
      
  # Now process states    
  if (next_alarm is not None):
    delta = int(next_alarm.strftime('%s')) - int(datetime.datetime.now().strftime('%s'))
    #print delta
    if (delta < -3600):
      print "It's been an hour, clearing alarm"
      buzzer_queue.put("beep_thrice")
      state = "No-Alarm"
      next_alarm = None
      snooze_until = None
      # Switch off Radio
      sonos_queue.put("Stop")
    elif (delta <= 0):
      if (state != "Alarm" and state != "Snooze"):
        print "Alarm - Setting State"
        state = "Alarm"
        sonos_queue.put("Alarm")
    # Beep a minute before alarm
    elif (delta <=60):
       if (warned == "No" and state != "Snooze"):
        buzzer_queue.put("beep_once")
        warned = "Yes"
    # Should be 599 for production
    elif (delta <= 299):
      if (state != "Pre-Alarm" and state != "Snooze"):
        print "Pre-Alarm - Setting state"
        state = "Pre-Alarm"
        sonos_queue.put("Pre-Alarm")
        light_queue.put("Pre-Alarm")
    elif (delta <= 599):
      if (state != "Pre-Pre-Alarm"  and state != "Pre-Alarm" and state != "Snooze"):
        print "Pre-Pre-Alarm - Setting State"
        state = "Pre-Pre-Alarm"
        buzzer_queue.put("beep_once")
    # Over a day for the next alarm?
    elif (delta >= 86400):
      if (state != "No-Alarm"):
        print ">24hr No Alarm - Setting state"
        state = "No-Alarm"
    else:
      state = "Clear"
  else:
    state = "No-Alarm"
    
  try:
    # Set fixed decimal, top right of display
    if (ntp_bad==1):
      #print "Got bad NTP, displaying"
      clock_segment.set_fixed_decimal(1)
    elif (ntp_bad==2):
      #print "Got bad comms, displaying"
      clock_segment.set_fixed_decimal(int(time.time() % 2))
    else:
      clock_segment.set_fixed_decimal(0)
    
    clock_segment.print_number_str(display_text(datetime.datetime.now()))
    
    # set brightness
    clock_segment.set_brightness(brightness)
    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    clock_segment.write_display()
    alarm_segment.clear()
    if (state == "Clear"):
      alarm_segment.set_colon(True) 
      alarm_segment.print_number_str(display_text(next_alarm))
    elif (state == "Pre-Alarm" or state == "Pre-Pre-Alarm"):     
      alarm_segment.set_colon(True) 
      alarm_segment.print_number_str(display_text_seconds(delta))
    elif (state == "Alarm"):
      if (int(round(time.time() * 1000))%1000 > 500):
        alarm_segment.set_colon(True) 
        alarm_segment.print_number_str(display_text(next_alarm))  
      else:
        alarm_segment.set_colon(True) 
        alarm_segment.print_number_str("")
    elif (state == "Snooze"):
      alarm_segment.set_colon(True) 
      alarm_segment.print_number_str(display_text_seconds(snoozedelta))
    else:
      alarm_segment.set_colon(False) 
      alarm_segment.print_number_str("----")
    
    
    alarm_segment.set_brightness(brightness)
    alarm_segment.write_display() 
  except Exception as e:
    print "Error handling LCD"
    print str(e)
  
  if (process_check < time.time()):
    process_check = time.time()+60
    if (not distance_process.is_alive()):
      print "Distance process has failed, respawning"
      distance_queue = Queue()
      distance_process = Process(target=sensor_distance.check_distance, args=(distance_queue,buzzer_queue,light_queue))
      distance_process.daemon = True
      distance_process.start()
      print "-> distance PID", distance_process.pid
  
  # Wait
  if (state == "Alarm"):
    time.sleep(0.1)
  else:
    time.sleep(0.5)
