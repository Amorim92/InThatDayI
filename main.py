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

# import frontend.server
#import tfidf
import face
import g_calendar
import g_drive
import g_gmail
import g_plus
import mail
#import twitter


def main():

# GOOGLE CONNECTION
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

#  FACEBOOK CONNECTION
    FB_TOKEN = 'CAAE2UVnAT0wBAMrfbuY2GVCeLUqebZCx7Vdj4v1LoEMpsV3kM9dTZAVJdN93pns5uISdvHMtXPfOOZAQd8jbIc1mTCFQOmoOJgTeMsKe7Ht2ey8uVcANUpCMfzf7jZAVPiwZBtRDcgSMZAl3elcvBeCNZCxQRjmaxZBi9C98JrI2HhJx2G4Oc86gDNyI6E8dctqDZBl1ewHZBgkBxqUNRxWHmX'
    FB_APP_ID = '341198002736972'
    FB_APP_SECRET = '027d3227a23c2798ef005d2b407febf1'

    # Use Facebook Graph API
    facebook_service = facebook.GraphAPI(FB_TOKEN)
    # Convert short live token to long live token
    token = facebook_service.extend_access_token(app_id = FB_APP_ID,
                                      app_secret = FB_APP_SECRET)['access_token']
    facebook_service.access_token = token
    

    # Authenticate and construct services
    calendar_service = build('calendar', 'v3', http = http)
    drive_service = build('drive', 'v2', http = http)
    gmail_service = build('gmail', 'v1', http = http)
    plus_service = build('plus', 'v1', http = http)


    # Generate dates
    now = datetime.datetime.now()
    currentMonth = now.month
    currentYear = now.year
    monthDays = calendar.monthrange(currentYear, currentMonth)

    before = datetime.datetime(currentYear, currentMonth, monthDays[1]).strftime("%Y-%m-%d")
    after = datetime.datetime(currentYear, currentMonth, 1).strftime("%Y-%m-%d")

    while(1):

        # colocar processos - nao foi possivel devido a chamadas das APIs
        # try:
        print before
        print after


        # Google Calendar API
        # c_IDs, c_status, c_summaries, c_creators, c_created, c_start, c_end = g_calendar.extract_events(calendar_service, '', before, after)
        # print c_IDs print c_status print c_summaries print c_creators print c_created print c_start print c_end
        # Call TF IDF if we have results
        # if c_summaries:
        #     tfidf.compute_tfidf(c_summaries)
        #     for summary in c_summaries:
        #         print summary
        #         tfidf.delete_stopwords(summary)


        # Database storage

        # To clean the arrays
        # g_calendar.clean()
       

        # for day in c_created:
        #     if after <= day <= before:
        #         print 'ola'

        # calendar_db.insert({'x': 1})

        # for c in calendar_db.find():
        #     print c

        # Google Drive API
        # d_IDs, d_titles, d_owners, d_created = g_drive.extract_documents(drive_service, '', before, after)
        # print d_IDs print d_titles print d_owners print d_created
        # Call TF IDF if we have results
        # if d_titles:
        
        # Database storage
        # To clean the arrays
        # g_drive.clean()


        # try:
        #     i, j = hillupillu()
        # except ValueError:
        #     print("Hey, I was expecting two values!")
        # To clean the arrays
        #g_drive.clean()


        # example query after: yyyy/mm/dd before:2015/1/1 after:2014/12/1
        # Google Gmail API
        query = 'before:' + str(before) + ' after:' + str(after)
        m_IDs, m_subjects, m_from, m_to, m_dates = g_gmail.extract_mails(gmail_service, query, '')

        # Call TF IDF if we have results
        # if p_publications:
        
        # Database storage
        # print m_IDs
        # To clean the arrays
        g_gmail.clean()

        # Google Plus API
        # p_IDs, p_publications, p_actors, p_urls, p_created = g_plus.extract_publications(plus_service, '', before, after)
        # print p_IDs print p_publications print p_actors
        
        # Call TF IDF if we have results
        # if p_publications:
        
        # Database storage

        # To clean the arrays
        # g_plus.clean()


        # Facebook API
        # f_IDs, f_messages, f_created = face.extract_posts(facebook_service, '', before, after)


        # Recalculate month and year
        if currentMonth - 1 < 1:
            currentMonth = 12
            # Year only goes until 1900, restart year value
            if currentYear - 1 < 1970:
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
        
        # except:
        #     print "Access token expired, wait a moment to refresh it."
        #     exit()
import cProfile
import re

cProfile.run('main()','restats')


if __name__ == '__main__':
    main()