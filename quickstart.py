from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'




def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    print('b0')
    home_dir = os.path.expanduser('~')
    print('b1')
    credential_dir = os.path.join(home_dir, '.credentials')
    print('b2')
    if not os.path.exists(credential_dir):
        print('b3')
        os.makedirs(credential_dir)
        print('b4')
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
    print('b5')

    store = Storage(credential_path)
    print('b6')
    credentials = store.get()
    print('b7')
    if not credentials or credentials.invalid:
        print('b8')
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        print('b9')
        flow.user_agent = APPLICATION_NAME
        print('b10')
        if flags:
            credentials = tools.run_flow(flow, store, flags)
            print('b11')
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
            print('b12')
        print('Storing credentials to ' + credential_path)
        print('b13')
    return credentials

def create_event():
    # Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)


    event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2018-03-03T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2018-03-03T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' %  ( event.get('htmlLink') ))
    
def make_calendar(name):
    print(name)
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    calendar = {
        'summary': name,
        'timeZone': 'America/Los_Angeles'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    #print (created_calendar['id'])

#function for retrieving id given summary/name of specific calendar
def find_id(summary):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    answer = {}
    page_token = None
    cal_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in cal_list['items']:
        answer[calendar_list_entry['summary'] ] = calendar_list_entry['id']
   
    return answer[summary]

#adding users to a specific calendar, given user info and nume of calendar
def add_user(name, calendar):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    rule = {
        'scope': {
            'type': 'user',
            'value': name,
        },
        'role': 'writer'
    }
   
    #store all the callendars in list item

    #do comparisoin
    #store in a hash map
    cal_id =find_id(calendar)
    created_rule = service.acl().insert(calendarId= cal_id , body=rule).execute()
    print (created_rule['id'])

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 2 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=2, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    

if __name__ == '__main__':
   # main()
    #create_event()
    make_calendar("puppies")
    #find_id("favorites")
    add_user("hannae.sya17@gmail.com","puppies")
