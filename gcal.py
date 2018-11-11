
#from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from cfgmgr import get_config
cfg = get_config()

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ', credential_path
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    
    f = open('nextalarm.txt', 'r')
    print f.readline()
    f.close()
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print 'Getting the upcoming 10 events' 
    eventsResult = service.events().list(
        calendarId=cfg['calendar']['id'], timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    else:
        event = events[0]
        start = event['start'].get('dateTime', event['start'].get('date'))
        print type(start)
        #startdate = datetime.datetime.strptime('2017-09-29 15:52:00','%Y-%m-%d %H:%M:%S')
        #startdate = datetime.datetime.strptime("2017-09-30T08:30:00+01:00",'%Y-%m-%dT%H:%M:%S%z')
        startdate = dt_parse(start)
        #2017-09-30T08:30:00+01:00
        print type(startdate)
        print startdate
        # event['summary'] is description. Don't see a need for that at the moment
        print start
        f = open('nextalarm.txt', 'w')
        f.write(start)
        f.close()


def dt_parse(t):
    # Example: 2017-09-30T08:30:00+01:00
    print t
    print t[0:19]
    print t[19]
    print t[20:25]
    ret = datetime.datetime.strptime(t[0:19],'%Y-%m-%dT%H:%M:%S')
    
    if t[18]=='+':
        ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    elif t[18]=='-':
        ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
    return ret
        
if __name__ == '__main__':
    main()