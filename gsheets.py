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

### Google Sheets Spreadsheet ID
SPREADSHEET_NAME = "Sensors"
SPREADSHEET_ID = "188_M8F_5TWVuvWKsviKfyvFv2qjLqETryw3zu9CjjZ4"

def init():
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

    return apiclient.discovery.build(
        'sheets',
        'v4',
        http=creds.authorize(httplib2.Http()),
        discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')


def upload_values( values ):
    service = init()
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='%s!A1' % SPREADSHEET_NAME,
        valueInputOption='USER_ENTERED',
        body={ 'values': [ values ] }).execute()

if __name__ == '__main__':
    upload_values( sys.argv[1:] )
