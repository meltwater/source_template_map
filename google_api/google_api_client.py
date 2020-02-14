import os
import datetime
import pickle
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

today = datetime.datetime.now()

#google stuff
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']


def google_creds():
    #handles authorization via OAuth client token related to meltwater google user account, will prompt authorization if no token is available, requires secret file for OAuth client
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./google_api/client_secret.json', SCOPES)
            creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def json_serialize_prep(l):
    #prepares data for json serialization (datetime objects, Decimals can not be json serialized), reformats types, returns list
    if any(isinstance(x, datetime.datetime) for x in [item for sublist in l for item in sublist]):
        l = [[x.isoformat() if isinstance(x, datetime.datetime) else str(x) for x in i] for i in l]
        return l
    else:
        return l

def create_new_spreadsheet():
    #creates new spreadsheet, returns spreadsheet id

    service = discovery.build('drive', 'v3', credentials=google_creds())

    title = 'News Content Monitoring - {}'.format(datetime.datetime.strftime(today, '%B %Y'))

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

    sheet_ids = [0, 1932773406, 1017799133, 57428055, 123309307, 1590255939, 2050389803]

    request_body = {
        'destination_spreadsheet_id': new_spreadsheet
    }
    for sheet_id in sheet_ids:
        request = service.spreadsheets().sheets().copyTo(spreadsheetId=old_sheet, sheetId=sheet_id, body=request_body)
        response = request.execute()

        print(response)

def add_rows(range, l):
    #checks range for present data, then appends new data underneath

    service = build('sheets', 'v4', credentials=google_creds())

    request_body = {
        'range': range,
        'majorDimension': 'ROWS',
        'values': l
        }

    request = service.spreadsheets().values().append(spreadsheetId=new_spreadsheet, range=range, valueInputOption='RAW', body=request_body)
    response = request.execute()

def overwrite_rows(spreadsheetid, range, l):
    #clears range and then inserts new data in its place
    service = build('sheets', 'v4', credentials=google_creds())

    clear_body = {
            'ranges': [ json_serialize_prep(l) ]

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
                    'values':
                    l

                    }
              ]
            }
    #print(request_body)
    request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetid, body=request_body)

    response =  request.execute()
    #print(response)

def get_value(range):

    service = build('sheets', 'v4', credentials=google_creds())

    request = service.spreadsheets().values().get(spreadsheetId=old_sheet, range=range)

    response = request.execute()
    print(response)

    return response['values']

def put_value(range, l):

    service = build('sheets', 'v4', credentials=google_creds())

    if len(row) == 1:
        row = [l]

    request_body = {
        'majorDimension': 'ROWS',
        'range': range,
        'values' :  l
    }

    request = service.spreadsheets().values().update(spreadsheetId=new_spreadsheet, range=range, body=request_body, valueInputOption='RAW')
    response = request.execute()
