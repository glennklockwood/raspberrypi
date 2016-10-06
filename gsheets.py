#!/usr/bin/env python
"""
Very simple shim to upload sensor readings to a Google Sheets using the Google
API.  Assumes that write permissions and the associated OAuth credentials have
been cached in ~/.credentials/sheets.googleapis.com-python-quickstart.json
"""

import os
import sys
import json

### Requirements for Google API 
import httplib2
import apiclient
import oauth2client.file

def _get_creds():
    """
    Retrieve credentials that are cached locally.  They are not present, the
    app must go through authentication and authorization to retrieve these
    credentials.  That process is demonstrated using quickstart.py which is
    available at https://developers.google.com/sheets/quickstart/python
    """
    cred_path = os.path.join( os.path.expanduser('~'),
                              '.credentials',
                              'sheets.googleapis.com-python-quickstart.json')
    creds = oauth2client.file.Storage(cred_path).get()
    if not creds or creds.invalid:
        raise Exception("Invalid credentials; you must re-authenticate")

    return creds

def upload_values( values, spreadsheet_id, sheet_name ):
    creds = _get_creds()
    http = creds.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')

    body = { 'values': [ values ] }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='%s!A1' % sheet_name,
        valueInputOption='USER_ENTERED',
        body=body).execute()

if __name__ == "__main__":
    creds = _get_creds()
    http = creds.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')

    chart_id = 336402020 # no idea how to get this through the API
    sheet_id = 0

    batch_body = {
        'requests': [
            {
                "updateChartSpec": {
                    "chartId" : chart_id,
                    "spec": {
                        "basicChart": {
                            "series": [
                                {
                                    "series": {
                                        "sourceRange": {
                                            #Sensors!A1:A2792, Sensors!E1:E2792
                                            "sources": [
                                                {
                                                    "sheetId": sheet_id,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 0,
                                                    "endColumnIndex": 1,
                                                },
                                                {
                                                    "sheetId": sheet_id,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 4,
                                                    "endColumnIndex": 5,
                                                },
                                            ],
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            },
        ],
    }
    result = service.spreadsheets().batchUpdate(
        spreadsheetId='188_M8F_5TWVuvWKsviKfyvFv2qjLqETryw3zu9CjjZ4',
        body=batch_body).execute()
