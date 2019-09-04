# Python Alarm Clock 

Python Alarm Clock is a Raspberry Pi based Alarm clock. Because why you wouldn't you want your alarm clock to run Python? 

While obviously a geeky project, there are advantages, such as the ability to adjust the wake up time via Google Calender, tie in to a home automation system, connect to a Sonos and play the radio at exactly the volume you want (Well, agreed with your wife...) when you go to bed. Wake you up with smart lights. Well, the list goes on...

Inputs

  - Google Calender to set the alarms (Works really well, allows you to easily set repeat appointments (I get up at 7:30 Monday-Thursday, but 8:00 on Friday) 
  - TSL2561 Lux Sensor (Dims Display)
  - VL53L0X Distance Sensor (Wave hand in vague direction of clock rather than finding button, however these were found to occationally misread maybe once every 2 weeks and do things like turning lights on in the middle of the night...) or Buttons (I've worked around 16mm Illuminated Pushbutton)
  - HTTP Server to collect messages from home automation system (Our heating is noisy, so it sends message to turn up the radio)

Outputs

  - Adafruit 7 Segment Displays x 2 - One showing the current time, one the currently set alarm time
  - Sonos - Connects via jishi/node-sonos-http-api - used for a radio, plus alarm
  - Smart Bulb - Makes a call via home assistant
  - Coffee Machine - Call via home assistant
  - Buzzer - I used an ADA1536 "Continuous tone" buzzer. Used as a backup should the unit be unable to connect to the Sonos


# Code

  - This is my first python project, so code quality probably isn't the best...
  - Python 2
  - I've used multiprocess and queue as a message passing interface. Primarily because it made more sense to me than threading, but also because it introduces fault tolerance (Of course, I could just do error handling...) If the Lux sensor process fails, then the odds are others will be fine
  - Multiprocess by it's nature has made the code reasonably module / plugable, for example swapping out the distance sensor for buttons was pretty easily

# Deployment
  - This code is on github for backup reasons as much as anything
  - Lots of hard coded values
  - Setup around my Home automation config. But you can probably plug things in easily enough
  - The required libraries should be findable from PIP

Notes
  - You'll find the Adafruit 7 Segment Displays reasonably bright in a dark room, even on the lowest setting
  - The VL53L0X was somewhat inconsistent and was badly affected by dust. It caused a number of false signals
  - As the RPi doesn't have a backup RTC battery, I used I2C RTCs to ensure that the devices could recover from a power outage without need for the internet to come back up for NTP. 
