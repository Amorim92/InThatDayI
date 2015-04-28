import os

filelist = [ f for f in os.listdir(".") if f.endswith(".pyc")]
for f in filelist:
    os.remove(f)

import datetime
import calendar

import httplib2
import time
import facebook


from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.util import scopes_to_string
from oauth2client.tools import run
from connect_db import connection

#import tfidf
import face
import g_calendar
import g_drive
import g_gmail
import g_plus
#import twitter



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

    if credentials.access_token_expired:
        credentials.refresh(http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    print credentials.to_json()

    # Use Facebook Graph API
    graph = facebook.GraphAPI('CAAE2UVnAT0wBAMrfbuY2GVCeLUqebZCx7Vdj4v1LoEMpsV3kM9dTZAVJdN93pns5uISdvHMtXPfOOZAQd8jbIc1mTCFQOmoOJgTeMsKe7Ht2ey8uVcANUpCMfzf7jZAVPiwZBtRDcgSMZAl3elcvBeCNZCxQRjmaxZBi9C98JrI2HhJx2G4Oc86gDNyI6E8dctqDZBl1ewHZBgkBxqUNRxWHmX')
    
    # Authenticate and construct services
    calendar_service = build('calendar', 'v3', http = http)
    drive_service = build('drive', 'v2', http = http)
    gmail_service = build('gmail', 'v1', http = http)
    plus_service = build('plus', 'v1', http = http)

    now = datetime.datetime.now()
    currentMonth = now.month
    currentYear = now.year
    monthDays = calendar.monthrange(currentYear, currentMonth)

    before = datetime.datetime(currentYear, currentMonth, monthDays[1]).strftime("%Y-%m-%d")
    after = datetime.datetime(currentYear, currentMonth, 1).strftime("%Y-%m-%d")

    # print before
    # print after

    while(True):

        # colocar processos - nao foi possivel devido a chamadas das APIs
        try:
        
            # DONE
            # c_IDs, c_status, c_created, c_summaries, c_creators, c_start, c_end = g_calendar.extract_events(calendar_service, '', before, after)
            # To clean the arrays
            # g_calendar.clean()
           


            # for day in c_created:
            #     if after <= day <= before:
            #         print 'ola'

            # calendar_db.insert({'x': 1})

            # for c in calendar_db.find():
            #     print c

            # DONE
            # d_IDs, d_titles, d_created, d_owners = g_drive.extract_documents(drive_service, '', before, after)
            # To clean the arrays
            # g_drive.clean()


            # try:
            #     i, j = hillupillu()
            # except ValueError:
            #     print("Hey, I was expecting two values!")
            # To clean the arrays
            #g_drive.clean()


            # example query after: yyyy/mm/dd before:2015/1/1 after:2014/12/1
            # done
            query = 'before:' + str(before) + ' after:' + str(after)
            # print query
            m_IDs, m_subjects, m_from, m_to, m_dates = g_gmail.extract_mails(gmail_service, query, '')
            g_gmail.clean()



            # DONE
            # p_IDs, p_publications, p_actors, p_urls, p_created = g_plus.extract_publications(plus_service, '', before, after)
            # To clean the arrays
            # g_plus.clean()


            
            #f_IDs, f_messages, f_created = face.extract_posts(graph)


            # Recalculate month and year
            if currentMonth - 1 < 1:
                currentMonth = 12
                # Year only goes until 1900, restart year value
                if currentYear - 1 < 1900:
                    now = datetime.datetime.now()
                    currentMonth = now.month
                    currentYear = now.year
                    monthDays = calendar.monthrange(currentYear, currentMonth)
                    before = datetime.datetime(currentYear, currentMonth, monthDays[1]).strftime("%Y-%m-%d")
                    after = datetime.datetime(currentYear, currentMonth, 1).strftime("%Y-%m-%d")
                else:
                    currentYear -= 1
                    monthDays = calendar.monthrange(currentYear, currentMonth)
            else:
                currentMonth -= 1
                monthDays = calendar.monthrange(currentYear, currentMonth)
            
            before = datetime.datetime(currentYear, currentMonth, monthDays[1]).strftime("%Y-%m-%d")
            after = datetime.datetime(currentYear, currentMonth, 1).strftime("%Y-%m-%d")

            # print before
            # print after
            print '----------------------------------------------------'
            #time.sleep(1*60)
        
        except:
            print "Access token expired, wait a moment to refresh it."
            exit()

if __name__ == '__main__':
    main()