import sys
from apiclient import errors

# Messages IDs, subjects and dates
messages_IDs = []
subjects = []
dates = []


def extract_subjects(service, token):

    try:
        # Result from Gmail API call
        response = service.users().messages().list(userId = 'me', includeSpamTrash = True,
                                                   maxResults = 100, pageToken = token).execute()

        # Append the ID of each message to messages_IDs
        if 'messages' in response:
            for message in response['messages']:
                messages_IDs.append(message['id'])

        while 'nextPageToken' in response:
            token = response['nextPageToken']

            # Call function with page token
            extract_subjects(service, token)

        print messages_IDs
        
        for id in messages_IDs:
            # Result from Gmail API call
            response = service.users().messages().get(userId = 'me', id = id, format = 'metadata',
                                                      metadataHeaders = ['From', 'To', 'Subject', 'Date'],
                                                      fields = 'payload').execute()

            # Append the subject and date of each message to subjects and dates
            while 'payload' in response:
                if 'headers' in response['payload']:
                    for header in response['payload']['headers']:
                        if header['name'] == 'Subject':
                            subjects.append(header['value'].encode('utf-8'))
                        if header['name'] == 'Date':
                            dates.append(header['value'])

        print subjects
        print dates

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        