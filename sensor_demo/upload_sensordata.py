#!/usr/bin/env python
"""
Very simple program to upload sensor readings to a Google Sheets using the
Google API.  Assumes that write permissions and the associated OAuth credentials
have been cached in ~/.credentials/sheets.googleapis.com-python-quickstart.json

Note that you should NOT import this script and make repeated calls to it from
another Python application; run this script as a subprocess instead.  The Google
API Python client seems to have memory leaks in it which will cause your
application to eventually crash if it makes too many API calls.
"""

import os
import sys
import json

### Requirements for Google API 
import httplib2
import apiclient
import oauth2client.file

### Google Sheets Spreadsheet ID
CREDENTIAL_FILE = os.path.join( os.path.expanduser('~'),
                                  '.credentials',
                                  'sheets.googleapis.com-python-quickstart.json')
SPREADSHEET_NAME = "Sensors"
CHART_NAME = "Both Sensors - Line"
SPREADSHEET_ID = "188_M8F_5TWVuvWKsviKfyvFv2qjLqETryw3zu9CjjZ4"

class SensorDataSpreadsheet(object):
    def __init__(self, spreadsheet_id):
        """
        Retrieve credentials that are cached locally.  They are not present, the
        app must go through authentication and authorization to retrieve these
        credentials.  That process is demonstrated using quickstart.py which is
        available at https://developers.google.com/sheets/quickstart/python
        """
        creds = oauth2client.file.Storage(CREDENTIAL_FILE).get()
        if not creds or creds.invalid:
            raise Exception("Invalid credentials; you must re-authenticate")

        self.spreadsheet_id = spreadsheet_id
        self.service = apiclient.discovery.build(
            'sheets',
            'v4',
            http=creds.authorize(httplib2.Http()),
            discoveryServiceUrl='https://sheets.googleapis.com/$discovery/rest?version=v4')

    def append_values( self, target_sheet_title, values ):
        """
        Use the append call to upload data to a Sheet.  Note that append has some
        curious semantics that don't always add the data to the end of the
        spreadsheet; instead, it looks for empty rows that would signal the end of
        a logical table of values that is embedded within the larger sheet.
        The documentation on this behavior is here:
    
        https://developers.google.com/sheets/guides/values#appending_values
        """
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='%s!A1' % target_sheet_title,
            valueInputOption='USER_ENTERED',
            body={ 'values': values }).execute()

    def reset_chart_ranges( self, target_chart_title ):
        """
        Deletes the upper bound on all chart data ranges, causing Sheets to reset
        and capture all data in the columns provided.  Useful for updating a chart
        after new columns are appended.
    
        Unfortunately only accepts basicChart types due to limitations in the
        Google Sheets API.
        """
        ### this has everything we need to know about the sheet (except its values)
        

        ### find our chart to update.  this assumes that the chart is either in
        ### its own sheet, or it is embedded in another sheet but is the only
        ### (or first) embedded chart
        target_chart = {}
        for sheet in self.sheet_spec()['sheets']:
            if 'charts' in sheet and 'properties' in sheet:
                if sheet['properties']['title'] == target_chart_title:
                    target_chart["chartId"] = sheet['charts'][0]["chartId"]
                    target_chart["spec"] = sheet['charts'][0]["spec"]
                    break

        ### reset the upper bound for the x values (domain)
        if 'basicChart' not in target_chart['spec']:
            raise Exception("Selected chart isn't supported by Google Sheets API")
        target_chart['spec']['basicChart']['domains'][0]['domain']['sourceRange']['sources'][0].pop('endRowIndex')

        ### reset the upper bound for the y values (series)
        for series in target_chart['spec']['basicChart']['series']:
            series['series']['sourceRange']['sources'][0].pop('endRowIndex')

        ### stick our modified chart into a request body
        body = {
            "requests": [
                {
                    "updateChartSpec": target_chart,
                },
            ],
        }

        ### submit our modified chart as a request
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,body=body).execute()

    def sheet_spec( self ):
        """Return the API's representation of an entire spreadsheet document"""
        return self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()

    def add_new_rows( self, target_sheet_title, count=1 ):
        """Add new rows to the bottom of an existing spreadsheet"""
        ### Find the sheet dimension for a sheet matching target_sheet_title
        target_sheet = None
        for sheet in self.sheet_spec()['sheets']:
            if ('properties' in sheet
            and sheet['properties']['title'] == target_sheet_title
            and 'gridProperties' in sheet['properties']):
                target_sheet = sheet
                break

        if sheet is None:
            raise Exception("Could not find target sheet")

        ### Create request to add a new row at the end of the sheet
        body = {
            "requests": [
                {
                    "appendDimension": {
                        "sheetId": sheet['properties']['sheetId'],
                        "dimension": "ROWS",
                        "length": count,
                    },
                },
            ],
        }
        ### Submit our request
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,body=body).execute()

    def row_count( self, target_sheet_title ):
        """Return the number of rows in a spreadsheet of a given title"""
        target_sheet = None
        for sheet in self.sheet_spec()['sheets']:
            if ('properties' in sheet
            and sheet['properties']['title'] == target_sheet_title
            and 'gridProperties' in sheet['properties']):
                target_sheet = sheet
                break

        if sheet is None:
            raise Exception("Could not find target sheet")
        else:
            return target_sheet['properties']['gridProperties']['rowCount']


    def add_values_at_end( self, target_sheet_title, values ):
        """Like append_values(), but explicitly adds rows to the bottom of the sheet
        and then fills them.  Bypasses the update API call's "table" finding within
        a spreadsheet."""
        body = { 'values': values }
        self.add_new_rows(target_sheet_title, len(values) )
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range="%s!A%d" % (target_sheet_title, self.row_count(target_sheet_title)),
            valueInputOption='USER_ENTERED',
            body=body).execute()


if __name__ == '__main__':
    ### Establish credentials to access the spreadsheet
    sensor_spreadsheet = SensorDataSpreadsheet(SPREADSHEET_ID)

    ### Upload new values to the absolute bottom of a spreadsheet
    if len(sys.argv[1:]) > 0:
#       sensor_spreadsheet.add_values_at_end(SPREADSHEET_NAME, [ sys.argv[1:] ])
        sensor_spreadsheet.append_values(SPREADSHEET_NAME, [ sys.argv[1:] ])

    ### Reset the bounds on the plot's x and y ranges to include the new data
    sensor_spreadsheet.reset_chart_ranges(CHART_NAME)
