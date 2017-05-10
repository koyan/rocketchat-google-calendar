from __future__ import print_function
import httplib2
import os
import requests
import json
import pickle
import os.path

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# your calendar ID. You can find it in the settings of the calendar
calendarId = ''

# the url where the webhook should be sent. You can find it when you create
# an incoming webhook (after you press save) in rocketchat->Administration->integrations
url = ''

# the timezone in which you want the events to appear. Example: "Europe/Athens" or "Europe/Amsterdam" or "Asia/Tokyo"
timeZone = ''

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
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Based upon the python tutorial for Google Calendar API.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # create the two datetime variables from which and to which we are checking the calendar
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    now_plus = (datetime.datetime.utcnow()+ datetime.timedelta(minutes = 30)).isoformat()+ 'Z'
    # print('now: ', now)
    # print('now_plus: ', now_plus)        
    # print('Getting the upcoming events')
    eventsResult = service.events().list(
        calendarId=calendarId, timeMin=now, timeMax=now_plus, singleEvents=True, timeZone=timeZone,
        orderBy='startTime').execute()
    if 'nextSyncToken' in eventsResult:
    	print('nextSyncToken: ',eventsResult['nextSyncToken'])
    	with open('nextSyncToken', 'w') as file:
		    file.write(eventsResult['nextSyncToken'])    #if eventsResult['nextPageToken']
    events = eventsResult.get('items', [])
    
    # read the list with the events that we have already sent
    # first check if the file exists
    if os.path.isfile('sentEvents'):
    	with open ('sentEvents', 'rb') as fp:
    		sentEvents = pickle.load(fp)
    else:
    	sentEvents = []

    # Define an empty list to put the events you just received
    # this will be saved as your new list so that you dont ever sent the same event twice
    sentEventsNew =[]

    for event in events:
        sentEventsNew.append(event['id'])
        if event['id'] not in sentEvents:
        	# uncomment the next two lines if you want to debug it in shell/terminal
        	# start = event['start'].get('dateTime', event['start'].get('date'))
        	# print(start, event['summary'])
        	payload = json.dumps(event)
        	# POST with form-encoded data
        	r = requests.post(url, data=payload)
        
    # save the new list of events (all in the next X minutes)
    # they have all been shown (either now or before, so this is our new list)
    with open('sentEvents', 'wb') as fp:
		pickle.dump(sentEventsNew, fp)
	
if __name__ == '__main__':
    main()