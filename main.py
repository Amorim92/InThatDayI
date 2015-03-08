from connect import connection
from authentication import authenticate
import calendar
import drive
import gmail
import plus
import time

def main():

    # Manage database
    totalCount_db, pcUser_db, calendar_db, drive_db, gmail_db, plus_db, lastFm_db, twitter_db, facebook_db = connection()

    # Authenticate and construct services
    calendar_service, drive_service, gmail_service, plus_service = authenticate()

    while(True):
        threads = gmail_service.users().threads().list(userId = 'me').execute()

        # Print ID for each thread
        if threads['threads']:
          for thread in threads['threads']:
            print 'Thread ID: %s' % (thread['id'])

        time.sleep(5*60)

if __name__ == '__main__':
  main()