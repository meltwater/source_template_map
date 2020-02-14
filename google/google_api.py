import os
import datetime
import pickle
import getpass
import json
import numpy
from math import isnan
from decimal import Decimal
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


#google authorization scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/calendar']

def read_calendar(cal, time_min, time_max):
    #reads calendar events for a certain timeframe from specified calendar
    if time_min == time_max:
        time_min = time_min.replace(hour=0,minute=0,second=0).isoformat()
        time_max = time_max.replace(hour=23,minute=59,second=59).isoformat()
    else:
        time_min = time_min.isoformat()
        time_max = time_max.isoformat()

    service = discovery.build('calendar', 'v3', credentials=google_creds())

    request = service.events().list(calendarId=cal, timeMin=time_min, timeMax=time_max, maxResults=30, singleEvents=True, orderBy='startTime')

    response = request.execute()

    return response['items']

def create_event(title, time_min, time_max, email, cal):
    #creates a single event, sets title and guest email
    service = discovery.build('calendar', 'v3', credentials=google_creds())

    request_body = {
        'summary' : title,
        'start' : {
            'date': datetime.datetime.strftime(time_min, "%Y-%m-%d")
        },
        'end' : {
            'date' : datetime.datetime.strftime(time_max, "%Y-%m-%d")
        },
        'attendees': [
            {'email' : email }
        ],

    }

    request = service.events().insert(calendarId=cal, body=request_body)

    response = request.execute()

    return response

def clear_events(cal, eventids):
    #deletes calendar events by id
    service = discovery.build('calendar', 'v3', credentials=google_creds())
    for id in eventids:
        request = service.events().delete(calendarId=cal, eventId=id)
        request.execute()



def google_creds(secret_file='client_secret'):
    #handles authorization via OAuth client token related to meltwater google user account, will prompt authorization if no token is available, requires secret file for OAuth client
    creds = None

    if os.path.exists('./google/token.pickle'):
        with open('./google/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./google/{}.json'.format(secret_file), SCOPES)
            creds = flow.run_console()
        with open('./google/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def json_serialize_prep(l):
    #prepares data for json serialization (datetime objects, Decimals can not be json serialized), reformats types, returns list
    if isinstance(l, list):
        if len(l) > 0:
            if isinstance(l[0], list):
                if any(isinstance(x, datetime.datetime) for x in [item for sublist in l for item in sublist]):
                    l = [[x.isoformat() if isinstance(x, datetime.datetime) else str(x) for x in i] for i in l]
                if any(isnan(x) for x in [item for sublist in l for item in sublist] if isinstance(x, float)):
                    print('NaN found')
                    l = [['Nan' if isnan(x) else x for x in i] for i in l]
                if any(isinstance(x, numpy.float64) for x in [item for sublist in l for item in sublist]):
                    l = [[float(x) if isinstance(x, numpy.float64) else x for x in i] for i in l]
                if any(isinstance(x, numpy.int64) for x in [item for sublist in l for item in sublist]):
                    l = [[int(x) if isinstance(x, numpy.int64) else x for x in i] for i in l]
                if any(isinstance(x, Decimal) for x in [item for sublist in l for item in sublist]):
                    l = [[int(x) if isinstance(x, Decimal) else x for x in i] for i in l]
                return l
            else:
                if any(isinstance(x, datetime.datetime) for x in l):
                    l = [x.isoformat() if isinstance(x, datetime.datetime) else str(x) for x in l]
                    return l
                else:
                    l = [str(x) for x in l]
                    return l
    else:
        return l

def create_new_spreadsheet():
    #creates new spreadsheet, returns spreadsheet id

    service = discovery.build('drive', 'v3', credentials=google_creds())

    #title = 'News Content Monitoring - {}'.format(datetime.datetime.strftime(today, '%B %Y'))

    request_body = {
        'name': title,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
            }
    #print(request_body)
    request = service.files().create(body=request_body, fields='id')
    response = request.execute()
    new_spreadsheet = response.get('id')
    print('Spreadsheet title: {}'.format(title))
    print('Spreadsheet ID: {}'.format(new_spreadsheet))
    print('Link to spreadsheet: https://docs.google.com/spreadsheets/d/{}/edit#gid=0'.format(new_spreadsheet))

    return new_spreadsheet

def copy_sheets(new_spreadsheet):
    #in progress

    service = discovery.build('sheets', 'v4', credentials=google_creds())

    #sheet_ids = [0, 1932773406, 1017799133, 57428055, 123309307, 1590255939, 2050389803]

    request_body = {
        'destination_spreadsheet_id': new_spreadsheet
    }
    for sheet_id in sheet_ids:
        request = service.spreadsheets().sheets().copyTo(spreadsheetId=old_sheet, sheetId=sheet_id, body=request_body)
        response = request.execute()

        print(response)

def add_rows(spreadsheetid, range, l, client_secret='client_secret'):
    #checks range for present data, then appends new data underneath

    service = build('sheets', 'v4', credentials=google_creds(client_secret))

    request_body = {
        'range': range,
        'majorDimension': 'ROWS',
        'values': json_serialize_prep(l)
        }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheetid, range=range, valueInputOption='RAW', insertDataOption='OVERWRITE', body=request_body)
    response = request.execute()

    return response

def overwrite_rows(spreadsheetid, range, l, client_secret='client_secret'):
    #clears range and then inserts new data in its place
    service = build('sheets', 'v4', credentials=google_creds(client_secret))

    clear_body = {
            'ranges': [ range ]

    }
    #print(clear_body)
    request = service.spreadsheets().values().batchClear(spreadsheetId=spreadsheetid, body=clear_body)

    response = request.execute()



    request_body = {
              'valueInputOption': 'USER_ENTERED',
              'responseDateTimeRenderOption': 'FORMATTED_STRING',
              'data': [
                  {
                    'range': range,
                    'majorDimension': 'ROWS',
                    'values': json_serialize_prep(l)

                    }
              ]
            }
    #print(request_body)
    request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=request_body)

    response =  request.execute()

    return response

def get_value(spreadsheetid, range, client_secret='client_secret'):

    service = build('sheets', 'v4', credentials=google_creds(client_secret))

    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetid, range=range)

    response = request.execute()

    return response['values']

def put_value(spreadsheetid, range, l, client_secret='client_secret'):

    service = build('sheets', 'v4', credentials=google_creds(client_secret))
    #print(json_serialize_prep(l))
    #for x in json_serialize_prep(l[0]):
    #    print('{}   {}'.format(x, type(x)))
    request_body = {
        'majorDimension': 'ROWS',
        'range': range,
        'values' :   json_serialize_prep(l)
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheetid, range=range, body=request_body, valueInputOption='RAW')
    response = request.execute()

    return response

def put_values(spreadsheetid, l, client_secret='client_secret'):

    service = build('sheets', 'v4', credentials=google_creds(client_secret))

    data = []
    for x in l:
        d = {
            'majorDimension': 'ROWS',
            'range': x[0],
            'values': json_serialize_prep(x[1])
        }
        data.append(d)

    request_body = {
        'valueInputOption': 'RAW',
        'data':  data
    }

    request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=request_body)
    response = request.execute()

    return response

def group_rows(spreadsheetid, sheetId, startIndex, endIndex, client_secret='client_secret'):

    service = build('sheets', 'v4', credentials=google_creds(client_secret))

    request_body = {
              "requests": [
                {
                  "addDimensionGroup": {
                    "range": {
                      "dimension": "ROWS",
                      "sheetId": sheetId,
                      "startIndex": startIndex,
                      "endIndex": endIndex
                    }
                  }
                }
              ]
            }

    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetid, body=request_body)

    response =  request.execute()

    return response
