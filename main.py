import os

filelist = [ f for f in os.listdir(".") if f.endswith(".pyc")]
for f in filelist:
    os.remove(f)


import httplib2

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.util import scopes_to_string
from oauth2client.tools import run
from connect_db import connection

import g_calendar
import g_drive
import g_gmail
import g_plus
import tfidf


def main():

     # Manage database
    totalCount_db, pcUser_db, calendar_db, drive_db, gmail_db, plus_db, lastFm_db, twitter_db, facebook_db = connection()

    # Path to client_secret file
    CLIENT_SECRET_FILE = 'C:\client_secret.json'
    # Google scopes used
    OAUTH_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
                    'https://www.googleapis.com/auth/drive.readonly',
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/plus.login',
                    'https://www.googleapis.com/auth/plus.me'
    ]

    # Location of the credentials storage file
    STORAGE = Storage('credentials.storage')

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()

    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope = scopes_to_string(OAUTH_SCOPES))
    http = httplib2.Http()

    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http = http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)
    
    print credentials.access_token_expired
    print credentials.to_json()
    
    # Authenticate and construct services
    calendar_service = build('calendar', 'v3', http = http)
    drive_service = build('drive', 'v2', http = http)
    gmail_service = build('gmail', 'v1', http = http)
    plus_service = build('plus', 'v1', http = http)

    while(True):
        #try:
            #g_calendar.extract_events(calendar_service)
            #g_drive.extract_files(drive_service)            
        g_gmail.extract_subjects(gmail_service, '')
            #g_plus.extract_cenas(plus_service)

       
        """except:
            print "Access token expired, wait a moment to refresh it."
            exit()"""

if __name__ == '__main__':
  main()