from __future__ import print_function
import datetime
import pytz
import pickle
import os.path
from AI import speak, get_audio
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENSIONS = ['rd', 'th', 'st', 'nd']
CALENDAR_STRINGS = ["what do i have", "do i have plans", "am i busy", "events"]
CREATE_EVENT_STRINGS = ["add an event", "add event"]
DATE_IDENTIFIER = ["next", "this", "tomorrow"] + DAYS + MONTHS
DELETE_EVENT_STRINGS = ["cancel event", "cancel all", "clear my schedule"]
SHOW_DATE = ["what is today's date", "show date", "what date is today"]
SHOW_TIME = ["what is the time", "what time is now", "show me the time", "tell me the time", "what is the current time", "tell me the curent time"]

TIME = {
        'morning': '8:00:00',
        'afternoon': '12:00:00',
        'evening': '6:00:00',
        'night': '9:00:00',
        'midnight': '23:59:00'
        }

TIMEZONE = 'Asia/Kolkata'

'''
EVENT = {
            'summary': 'Dinner with friends',
            'start': {'dateTime': '2019-11-20T19:00:00',
                      'timeZone': TIMEZONE},
            'end': {'dateTime': '2019-11-20T22:00:00',
                    'timeZone': TIMEZONE}
        }
'''


def authenticate_google():

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


service = authenticate_google()

def create_events(service, summary, date, time=None, duration=3, end=None):

    if not time:
        time = '00:00:00'
        end = '23:59:59'

    if not end:
        endtime = time.split(':')
        endtime[0] += duration
        end = ':'.join(endtime)

    EVENT = {
        'summary': summary,
        'start': {'dateTime': str(date) + 'T' + str(time),
                  'timeZone': TIMEZONE},
        'end': {'dateTime': str(date) + 'T' + str(end),
                'timeZone': TIMEZONE}
    }

    service.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()


def delete_event(text):

    date = get_date(text)
    if not date:
        return "Please mention the date correctly"

    event_Id = get_events(date, service, getId=True)

    if not event_Id:
        return "You have no events on this day"

    else:
        for id in event_Id:
            service.events().delete(calendarId='primary', eventId=id).execute()
        return "Your schedule has been cleared on {}".format(date)



def add_event():

    speak("Mention the date of the event")
    event_text = get_audio()

    date = get_date(event_text)

    if not date:
        return "Please Mention event date"

    speak("Mention the time of event")
    event_text = get_audio()
    temp = event_text.split()
    starttime, endtime = None, None

    for i in ['from', 'at', 'on']:
        if i in temp:
            prep = temp.index(i)
            summary = ' '.join(temp[:prep])
            starttime = get_time(' '.join(temp[prep + 1:]))
            if 'to' in temp:
                a = temp.index('to')
                endtime = get_time(' '.join(temp[a + 1:]))



    speak("What event should I add?")
    summary = get_audio()

    if not summary:
        return "Please mention details of the event"

    try:
        create_events(service, summary, date, time=starttime, end=endtime)
        return "Event Added to your Schedule"
    except:
        return "Please mention all details of the event"



def get_events(day, service, getId=False):

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        if getId:
            return '0'
        return ['No upcoming events found.']

    else:
        voice = ["You have {} events on this day".format(len(events)) if len(events) > 1 else "You have 1 event on this day"]

    ev_id = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'], event['id'])
        start_time = str(start.split("T")[1].split("-")[0])
        if int(start_time.split(":")[0]) < 12:
            start_time += "am"
        else:
            start_time += "pm"

        if getId:
            ev_id.append(event["id"])
        voice.append(event["summary"] + " at " + start_time)

    if getId:
        return ev_id

    return voice

def get_date(text):

    today = datetime.date.today()

    if text.count == 'today':
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year += 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        diff = day_of_week - current_day_of_week

        if diff < 0:
            diff += 7
            if text.count("next"):
                diff += 7

        return today + datetime.timedelta(diff)

    if day != -1:
        return datetime.date(year=year, month=month, day=day)


def get_time(text):
    temp = text.split()
    if temp[0].isdigit():
        if int(temp[0]) <= 12 and 'pm' in temp:
            temp[0] = str(int(temp[0]) + 12)

        time = temp[0] + ':00:00'
        if temp[0] == '24':
            time = '23:59:00'
        return time
    for word in temp:
        if word in TIME:
            return TIME[word]


def event_manage(text):

    for phrases in CALENDAR_STRINGS:
        if phrases in text:
            return get_events(get_date(text), service)

    for phrase in CREATE_EVENT_STRINGS:
        if phrase in text:
            return add_event()

    for phrase in DELETE_EVENT_STRINGS:
        if phrase in text:
            return delete_event(text)

    for phrase in SHOW_DATE:
        if phrase in text:
            day = datetime.date.today().strftime("%D")
            #print(day)
            return "Today's date is " + str(day)

    for phrase in SHOW_TIME:
        if phrase in text:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            #print(time)
            return "The time is " + str(time)



def parse_datetime(text):

    temp = text.split()

    for phrases in CALENDAR_STRINGS:
        if phrases in text:
            return get_events(get_date(text), service)

    for phrases in CREATE_EVENT_STRINGS:

        if phrases in text:
            x = phrases.split()
            [temp.remove(i) for i in x]
            summary, starttime, endtime = ' '.join(temp), None, None
            for i in ['from', 'at', 'on']:
                if i in temp:
                    prep = temp.index(i)
                    summary = ' '.join(temp[:prep])
                    starttime = get_time(' '.join(temp[prep+1:]))
                    if 'to' in temp:
                        a = temp.index('to')
                        endtime = get_time(' '.join(temp[a+1:]))
            date = get_date(text)
            a = summary.split()

            for ph in DATE_IDENTIFIER:
                if ph in a:
                    a.remove(ph)
            summary = ' '.join(a)
            print(summary.capitalize(), starttime, endtime, date)

            try:
                create_events(service, summary, date, time=starttime, end=endtime)
                return "Event Added Successfully"
            except:
                return "Please mention all details of the event"


    return None



if __name__ == '__main__':

#    service.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()
#    event_Id = get_events(datetime.datetime.strptime('11-20-2019', '%m-%d-%Y').date(), service, getId=True)


    #print(parse_datetime("add an event Ice Skating this wednesday"))
    print(event_manage("what is today's date"))
    #print(parse_datetime("clear my schedule for this wednesday"))
'''    
    for id in event_Id[:-1]:
        service.events().delete(calendarId='primary', eventId=id).execute()
'''