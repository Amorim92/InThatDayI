import os

filelist = [ f for f in os.listdir(".") if f.endswith(".pyc")]
for f in filelist:
    os.remove(f)

import time, datetime, calendar

import httplib2
# import facebook, requests

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.util import scopes_to_string
from oauth2client.tools import run
from connect_db import connection

# import frontend.server
import tfidf
import face, g_calendar, g_drive, g_gmail, g_plus
import imaplib, email, getpass
# import mail
#import twitter


def main():

# GOOGLE CONNECTION
    # Manage collections
    total_db, terms_day_db, terms_week_db, terms_month_db, terms_year_db, people_db, dates_db = connection()

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

    # print credentials.to_json()

# FACEBOOK CONNECTION - not working because token expired and cannot be refreshed since it's a desktop app
    # FB_TOKEN = 'CAAE2UVnAT0wBAJ7T4wT2dYm1j5ZBQx5UZBcWqvWHtrc2pzED0YHkYHjZA4mr0PXXigVOg8HerZAAniChT9TgDrh4NZCtnUvW0QbWQE1dtQUw6ZAXmMBXy7MaMHagtXPZAe5oRLoMFiJhlhtmeTrsmJa68ow5dHdfDw3v10cEvOQDwNmqDscdfACP384BfMoz9c5dSOsapNZBm3F244QZAen03'
    # FB_APP_ID = '341198002736972'
    # FB_APP_SECRET = '027d3227a23c2798ef005d2b407febf1'

    # # Use Facebook Graph API
    # facebook_service = facebook.GraphAPI(FB_TOKEN)
    # # Convert short live token to long live token
    # token = facebook_service.extend_access_token(app_id = FB_APP_ID,
    #                                              app_secret = FB_APP_SECRET)['access_token']
    # facebook_service.access_token = token
    

    # Authenticate and construct services
    calendar_service = build('calendar', 'v3', http = http)
    drive_service = build('drive', 'v2', http = http)
    gmail_service = imaplib.IMAP4_SSL('imap.gmail.com')
    # email = raw_input("Email address: ")
    # gmail_service.login(email, getpass.getpass())
    # gmail_service.login('joao.ricardo.amorim.ja@gmail.com', getpass.getpass())
    plus_service = build('plus', 'v1', http = http)


    # Generate dates
    now = datetime.datetime.now()
    currentMonth = now.month
    currentYear = now.year
    monthDays = calendar.monthrange(currentYear, currentMonth)

    before = datetime.datetime(currentYear, currentMonth, monthDays[1]).strftime("%Y-%m-%d")
    after = datetime.datetime(currentYear, currentMonth, 1).strftime("%Y-%m-%d")

    # calendar_week = {'c_IDs': [], 'c_status': [], 'c_summaries': [], 'c_creators': [],
    #                  'c_created': [], 'c_start': [], 'c_end': []}

    # Year dictionaries
    calendar_year = {'c_IDs': [], 'c_status': [], 'c_summaries': [], 'c_creators': [],
                      'c_created': [], 'c_start': [], 'c_end': []}

    while(1):


        # colocar processos - nao foi possivel devido a chamadas das APIs
        # try:
        print before
        print after


        # Google Calendar API
        c_IDs, c_status, c_summaries, c_creators, c_created, c_start, c_end = g_calendar.extract_events(calendar_service, '', before, after)

        # print c_IDs print c_status print c_summaries print c_creators print c_created print c_start print c_end

        if c_summaries:

            # Save data to call yearly TF-IDF
            calendar_year['c_IDs'].extend(c_IDs)
            calendar_year['c_status'].extend(c_status)
            calendar_year['c_summaries'].extend(c_summaries)
            calendar_year['c_creators'].extend(c_creators)
            calendar_year['c_created'].extend(c_created)
            calendar_year['c_start'].extend(c_start)
            calendar_year['c_end'].extend(c_end)
            # print calendar_year


            # Call daily TF-IDF
            for currentDay in range(monthDays[1], 0, -1):
                
                calendar_day = {'c_IDs': [], 'c_status': [], 'c_summaries': [], 'c_creators': [],
                                'c_created': [], 'c_start': [], 'c_end': []}

                daily_date = datetime.datetime(currentYear, currentMonth, currentDay)

                day_of_week = daily_date.weekday()
                # print day_of_week
                delta_start = datetime.timedelta(days = day_of_week)
                week_start = daily_date - delta_start

                delta_end = datetime.timedelta(days = 6 - day_of_week)
                week_end = daily_date + delta_end

                # print beginning_of_week
                # print type(week_end)
                print daily_date

                for date in c_created:

                    if date[:10] == daily_date.strftime("%Y-%m-%d"):

                        c_index = c_created.index(date)

                        calendar_day['c_IDs'].append(c_IDs.pop(c_index))
                        calendar_day['c_status'].append(c_status.pop(c_index))
                        calendar_day['c_summaries'].append(c_summaries.pop(c_index))
                        calendar_day['c_creators'].append(c_creators.pop(c_index))
                        calendar_day['c_created'].append(c_created.pop(c_index))
                        calendar_day['c_start'].append(c_start.pop(c_index))
                        calendar_day['c_end'].append(c_end.pop(c_index))

                    if week_start.strftime("%Y-%m-%d") < date and date < week_end.strftime("%Y-%m-%d"):
                        print 'hello++++++++++++++++++++++'
                        print date
                        print 'hello++++++++++++++++++++++'

                    else:
                        continue

                # print calendar_day

                if calendar_day['c_summaries'] is not None:
                    calendar_daily = tfidf.compute_tfidf(calendar_day['c_summaries'], 'Google Calendar', calendar_day['c_IDs'],
                                                         calendar_day['c_creators'], calendar_day['c_created'], status=calendar_day['c_status'],
                                                         start=calendar_day['c_start'], end=calendar_day['c_end'])


                    # print calendar_daily

                    #     if currentDay + 1 > monthDays[1]:
                    #         currentDay = 1
                    #         break
                    #     else:
                    #         daily_date = datetime.datetime(currentYear, currentMonth, currentDay + 1).strftime("%Y-%m-%d")



            # Call monthly TF-IDF
            # calendar_insert_m = tfidf.compute_tfidf(c_summaries, 'Google Calendar', c_IDs, c_creators, c_created,
            #                                         status = c_status, start = c_start, end = c_end)
            # print calendar_insert


            # Database storage
            # for key in calendar_insert_m.keys():
            #     terms_m_db.insert(calendar_insert_m[key])
            # print terms_m_db.count()
            # print '================================================' 
            # insert_many([{'x': i} for i in range(2)], True)

            # terms_m_db, terms_y_db, people_db, dates_db

        # To clean the arrays
        g_calendar.clean()
       

        # for day in c_created:
        #     if after <= day <= before:
        #         print 'ola'

        # calendar_db.insert({'x': 1})

        # for c in calendar_db.find():
        #     print c

        # Google Drive API
        # d_IDs, d_titles, d_owners, d_created = g_drive.extract_documents(drive_service, '', before, after)
        # print d_IDs
        # print d_titles
        # print d_owners
        # print d_created
        
        # Call daily TF-IDF
        # if d_titles:
        #     drive_insert = tfidf.compute_tfidf(d_titles, 'Google Drive', d_IDs, d_owners, d_created)
            # print drive_insert
        
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
        # Google Gmail IMAP
        # query = 'before:' + str(before) + ' after:' + str(after)
        # m_IDs, m_subjects, m_from, m_to, m_dates = g_gmail.extract_mails(gmail_service, before, after)

        # Call TF IDF if we have results
        # if p_publications:
        
        # Database storage
        # print m_IDs
        # To clean the arrays
        # g_gmail.clean()

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

            # Call yearly TF-IDF
            # if calendar_year['c_summaries']:
            #     calendar_insert_y = tfidf.compute_tfidf(calendar_year['c_summaries'], 'Google Calendar', calendar_year['c_IDs'],
            #                                             calendar_year['c_creators'], calendar_year['c_created'], status=calendar_year['c_status'],
            #                                             start=calendar_year['c_start'], end=calendar_year['c_end'])
                # print c
            
            currentMonth = 12
                
            # Year only goes until 1990, restart year value
            if currentYear - 1 < 1990:
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


# import cProfile
# import re

# cProfile.run('main()','restats')


if __name__ == '__main__':
    main()