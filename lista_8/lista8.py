from datetime import datetime
import json
from math import floor
import requests
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import re

# przykład bez uwierzytelniania

url = "https://api.punkapi.com/v2/beers"

response = requests.get(url).text
response_info = json.loads(response)

print('{0: <2} {1: <35} {2: <60}'.format('Id', 'Name', 'Description'))
for id in range (0, len(response_info)):
    beer = response_info[id]
    print('{0: >2} {1: <35} {2: <60}'.format(id, beer['name'], beer['tagline']))

print('')

# przykład z uwierzytelnianiem

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def date_format(dateTime):
    pattern = "(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<min>\d{2}).*"
    res = re.match(pattern, dateTime)
    return res.group("day") + "." + res.group("month") + "." + res.group("year") + " " + res.group("hour") + ":" + res.group("min")

def fst_sentence_from_n_recent(n):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    events = service.events().list(calendarId='primary', maxResults=n, singleEvents=True, orderBy='startTime').execute()
    
    for event in events['items']:
        print ("{0: <30}  {1}".format(event['summary'], date_format(event['start']['dateTime'])))

fst_sentence_from_n_recent(5)