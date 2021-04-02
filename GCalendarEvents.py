from __future__ import print_function
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getEvents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/pi/token.json'):
        creds = Credentials.from_authorized_user_file('/home/pi/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/pi/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('/home/pi/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today  =datetime.today()

    now = datetime(today.year, today.month, today.day, hour = 0, minute=0).isoformat() + 'Z'
    tonight =  datetime(today.year, today.month, today.day, hour = 23, minute=59).isoformat() + 'Z'

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=tonight,
                                        maxResults=6, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return []
    else:
        return events

if __name__ == '__main__':
    events = getEvents()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_datetime = datetime.fromisoformat(start)
        print(start_datetime.strftime("%H:%M"), event['summary'])

