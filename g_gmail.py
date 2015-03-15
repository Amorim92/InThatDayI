from apiclient import errors

# Messages IDs, subjects and dates
messages_IDs = []
subjects = []
_from = [] 
_to = []
dates = []


def extract_subjects(service, token):

    try:
        # Result from Gmail API call
        mails = service.users().messages().list(userId = 'me', includeSpamTrash = True,
                                                maxResults = 100, pageToken = token).execute()
        if mails != None:
            # Append the ID of each message to messages_IDs
            if 'messages' in mails:
                for message in mails['messages']:
                    messages_IDs.append(message['id'])

            page_token = mails.get('nextPageToken')

            while page_token != None:
                # Call function with page page_token
                extract_subjects(service, page_token)

            print messages_IDs
            
            for id in messages_IDs:
                # Result from Gmail API call
                mails = service.users().messages().get(userId = 'me', id = id, format = 'metadata',
                                                       metadataHeaders = ['From', 'To', 'Subject', 'Date'],
                                                       fields = 'payload').execute()

                # Append the subject and date of each message to subjects and dates
                if 'payload' in mails:
                    if 'headers' in mails['payload']:
                        for header in mails['payload']['headers']:
                            if header['name'] == 'Subject':
                                subjects.append(header['value'].encode('utf-8'))
                                print subjects
                            if header['name'] == 'Date':
                                dates.append(header['value'])
                                print header['value']
                            if header['name'] == 'From':
                                _from.append(header['value'])
                                print header['value']
                            if header['name'] == 'To':
                                _to.append(header['value'])
                                print header['value']

        else:
            print "Bad mails to Gmail API service."

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        