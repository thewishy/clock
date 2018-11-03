# Python Alarm Clock 

Python Alarm Clock is a Raspberry Pi based Alarm clock. Because why you wouldn't you want your alarm clock to run Python? 

While obviously a geeky project, there are advantages, such as the ability to tie in to a home automation system, connect to a Sonos and play the radio at exactly the volume you want (Well, agreed with your wife...) when you go to bed. Wake you up with smart lights. Well, the list goes on...

Inputs

  - Google Calender to set the alarms (Works really well, allows you to easily set repeat appointments (I get up at 7:30 Monday-Thursday, but 8:00 on Friday) 
  - TSL2561 Lux Sensor (Dims Display)
  - VL53L0X Distance Sensor (Wave hand in vague direction of clock rather than finding button)
  - HTTP Server to collect messages from home automation system (Our heating is noisy, so it sends message to turn up the radio)

Outputs

  - Adafruit 7 Segment Displays x 2 - One showing the current time, one the currently set alarm time
  - Sonos - Connects via jishi/node-sonos-http-api - used for a radio, plus alarm
  - Smart Bulb - Makes a call via home assistant
  - Buzzer - I used an ADA1536 "Continuous tone" buzzer. Used as a backup should the unit be unable to connect to the Sonos


# Code

  - This is my first python project, so code quality probably isn't the best...
  - Python 2
  - I've used multiprocess and queue as a message passing interface. Primarily because it made more sense to me than threading, but also because it introduces fault tolerance (Of course, I could just do error handling...) If the Lux sensor process fails, then the odds are others will be fine

# Deployment
  - This code is on github for backup reasons as much as anything
  - Lots of hard coded values
  - Setup around my Home automation config. But you can probably plug things in easily enough
  - The required libraries should be findable from PIP