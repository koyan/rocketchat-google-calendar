import json, pickle, os.path, argparse, datetime
import requests, httplib2

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_args():
    args = argparse.ArgumentParser()
    args.add_argument('--auth_file', required = True, help = 'Full path to the json credentials file')
    args.add_argument('--delegated_user', required = True,
        help = 'Delegated Google user that has access to the calendar')
    args.add_argument('--calendar_id', required = True, help = 'Google calendar id from calendar settings')
    args.add_argument('--url', required = True, help = 'URL to send events to')
    args.add_argument('--time_zone', default = 'UTC',
        help = 'Time zone that events will appear in, defult is UTC')
    args.add_argument('--sent_data_file', default = 'sentEvents',
        help = 'Full path to the file where already processed events will be stored, defaults to ./sentEvents')
    return args.parse_args()

def get_service(json_auth_file, delegated_user):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_auth_file, scopes=SCOPES)
    delegated_credentials = credentials.create_delegated(delegated_user)
    http = delegated_credentials.authorize(httplib2.Http())
    return build('calendar', 'v3', http=http)

def main():
    """Based upon the python tutorial for Google Calendar API.
    """
    opts = get_args()
    service = get_service(opts.auth_file, opts.delegated_user)

    calendarId = opts.calendar_id
    url = opts.url
    timeZone = opts.time_zone

    # create the two datetime variables from which and to which we are checking the calendar
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    now_plus = (datetime.datetime.utcnow()+ datetime.timedelta(minutes = 30)).isoformat()+ 'Z'

    eventsResult = service.events().list(
        calendarId=calendarId, timeMin=now, timeMax=now_plus, singleEvents=True, timeZone=timeZone,
            orderBy='startTime').execute()

    events = eventsResult.get('items', [])

    # read the list with the events that we have already sent
    # first check if the file exists
    if os.path.isfile(opts.sent_data_file):
        with open (opts.sent_data_file, 'rb') as fp:
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
    with open(opts.sent_data_file, 'wb') as fp:
        pickle.dump(sentEventsNew, fp)

if __name__ == '__main__':
    main()
