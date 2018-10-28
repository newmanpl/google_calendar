from __future__ import print_function
import datetime, time
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import dateutil.parser
import vlc

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def run_vlc():
  instance = vlc.Instance()

  #Create a MediaPlayer with the default instance
  player = instance.media_player_new()

  #Load the media file
  media = instance.media_new('/home/my.mp3')

  #Add the media to the player
  player.set_media(media)

  #Play for 10 seconds then exit
  player.play()
  time.sleep(10)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret_google_calendar.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    start_date = datetime.datetime(
        2018, 10, 01, 00, 00) 
    start_date_sec = time.mktime(start_date.timetuple())
    end_date = datetime.datetime(2019, 10, 01, 00, 10 ) 
    end_date_sec = time.mktime(end_date.timetuple())

    print(end_date_sec - start_date_sec)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('----- Getting the upcoming 10 events -----')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    delta = 0
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #ds = dateutil.parser.parse(start).strftime('%Y-%m-%d %I:%M:%S')
        ds = dateutil.parser.parse(start)
        ds_s = time.mktime(ds.timetuple())
        current = datetime.datetime.now();
        current_s = time.mktime(current.timetuple())
        delta = current_s - ds_s
        print("delta = ", delta)
        print(start, event['summary'])
        print("----------------------------------")
    if delta > 0:
      run_vlc()

if __name__ == '__main__':
    main()
