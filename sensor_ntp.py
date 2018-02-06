from lib import notify_if_changed
import time
import subprocess

def check_ntp(queue):
  ntp_state = 1
  while(True):
    try:
      ntpstat = subprocess.check_output(['ntpstat', ''])
      ntpsplit = ntpstat.split()
      #print ntpsplit[0], ntpsplit[12]
      if ntpsplit[0] == 'synchronised' and int(ntpsplit[12]) < 150:
        #print "NTP OK"
        ntp_state = notify_if_changed(queue,ntp_state,0)
      else:
        print "NTP Poorly"
        ntp_state = notify_if_changed(queue,ntp_state,1)
    except:
      print "Error executing NTPStat"
      ntp_state = notify_if_changed(queue,ntp_state,1)

    time.sleep(300)