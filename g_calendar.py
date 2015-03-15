import sys
from apiclient import errors


#token
page_token = None
sync_token = None
# Messages IDs, subjects and dates
messages_IDs = []
subjects = []
dates = []


def extract_subjects(service):

    try:
        # Result from Gmail API call
        events = service.events().list(calendarId = 'primary', orderBy = 'startTime', pageToken = page_token,
                                       showDeleted = True, singleEvents= True, syncToken = sync_token,
                                       fields = 'items(creator(displayName,email),updated,created,summary,location,start,end),nextPageToken,nextSyncToken').execute()
        if events != None:
            # Append the ID of each message to messages_IDs
            if 'messages' in events:
                for message in events['messages']:
                    messages_IDs.append(message['id'])

            while 'nextPageToken' in events:
                token = events['nextPageToken']

                # Call function with page token
                extract_subjects(service, token)

            print messages_IDs
            
            for id in messages_IDs:
                # Result from Gmail API call
                events = service.users().messages().get(userId = 'me', id = id, format = 'metadata',
                                                          metadataHeaders = ['From', 'To', 'Subject', 'Date'],
                                                          fields = 'payload').execute()

                # Append the subject and date of each message to subjects and dates
                while 'payload' in events:
                    if 'headers' in events['payload']:
                        for header in events['payload']['headers']:
                            if header['name'] == 'Subject':
                                subjects.append(header['value'].encode('utf-8'))
                            if header['name'] == 'Date':
                                dates.append(header['value'])

            print subjects
            print dates
        else:
            print "Bad events to Gmail API service."

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        