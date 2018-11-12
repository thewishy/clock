import time
import datetime
from multiprocessing import Queue
from lib import notify_if_changed

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from cfgmgr import get_config
cfg = get_config()

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print "Credentials are bad"
    return credentials

def dt_parse(t):
    # Example: 2017-09-30T08:30:00+01:00
    ret = datetime.datetime.strptime(t[0:19],'%Y-%m-%dT%H:%M:%S')
    
    if t[18]=='+':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[18]=='-':
        ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret

def gcal(queue):
  alarm_time = None
  # Try to read from file (For reboot scenarios)
  try:
    f = open('nextalarm.txt', 'r')
    readfromfile = f.readline()
    f.close()
    alarm_time = notify_if_changed(queue,alarm_time,dt_parse(readfromfile))
  except:
    print "File handling error"
  # Test harness
  #alarm_time = notify_if_changed(queue,alarm_time,datetime.datetime.strptime('2017-09-30 15:52:00','%Y-%m-%d %H:%M:%S')) 
  
  
  while True:
    #print "Runnng GCAL"
    try:
      credentials = get_credentials()
      http = credentials.authorize(httplib2.Http())
      service = discovery.build('calendar', 'v3', http=http)

      now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
      #print 'Getting the upcoming alarm' 
      eventsResult = service.events().list(
          calendarId=cfg['calendar']['id'], timeMin=now, maxResults=1, singleEvents=True,
          orderBy='startTime').execute()
      events = eventsResult.get('items', [])

      if not events:
          print 'No upcoming events found.'
          alarm_time = notify_if_changed(queue,alarm_time,None)
          #print 'Notification complete'
      else:
          event = events[0]
          start = event['start'].get('dateTime', event['start'].get('date'))
          # event['summary'] is description. Don't see a need for that at the moment
          f = open('nextalarm.txt', 'w')
          f.write(start)
          f.close()
          alarm_time = notify_if_changed(queue,alarm_time,dt_parse(start))
      #time.sleep(30)
    except:
      print "GCAL Error"
    time.sleep(600)