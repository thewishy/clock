from lib import notify_if_changed
import time
import subprocess
import os

def check_ntp(queue):
  ntp_state = 1
  while(True):
    try:
    #if subprocess.call(["ping", "-c 1", "192.168.1.1",">/dev/null"]):
    #if subprocess.check_output(["ping", "-c 1", "192.168.1.1"]):
      if os.system("ping -c 1 192.168.1.1 >/dev/null"):
        print "Ping is bad"
        ntp_state = notify_if_changed(queue,ntp_state,2)
      else:
        #print "Ping is good"
        ntp_state = notify_if_changed(queue,ntp_state,0)
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
    except:
      print "Ping Broke"
      ntp_state = notify_if_changed(queue,ntp_state,2)
    
    


    time.sleep(300)
