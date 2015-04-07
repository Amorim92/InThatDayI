from apiclient import errors


# Messages IDs, subjects, from, to and sending dates
messages_IDs = []
subjects = []
_from = [] 
_to = []
_dates = []


def extract_mails(service, query, token):

    try:
        # Result from Gmail API call
        mails = service.users().messages().list(userId = 'me', includeSpamTrash = True, q = query,
                                                pageToken = token, fields = 'messages(id),nextPageToken').execute()


        # Append the ID of each message to messages_IDs
        if mails != None:
            if 'messages' in mails:
                for message in mails['messages']:
                    # Message ID
                    messages_IDs.append(message['id'])


            # Call function with page page_token
            if 'nextPageToken' in mails:
                token = mails['nextPageToken']
                extract_mails(service, query, token)

        else:
            print "Bad request to Gmail API service or there's no e-mails in your Gmail Account."
            return


        # Get data of each message ID
        for id in messages_IDs:
            # Result from Gmail API call
            messages = service.users().messages().get(userId = 'me', id = id, format = 'metadata',
                                                      metadataHeaders = ['From', 'To', 'Subject', 'Date'],
                                                      fields = 'payload').execute()


            # Append data of each message to the correspondent array
            if messages != None:
                if 'payload' in messages:
                    if 'headers' in messages['payload']:
                        for header in messages['payload']['headers']:
                            # Subject
                            if header['name'] == 'Subject':
                                subjects.append(header['value'].encode('utf8'))
                            else:
                                subjects.append('')

                            # Date
                            if header['name'] == 'Date':
                                _dates.append(header['value'][5:-6])
                            else:
                                _dates.append('')
                                #print header['value']

                            # From
                            if header['name'] == 'From':
                                _from.append(header['value'].encode('utf8'))
                            else:
                                _from.append('')
                                #print header['value']

                            # To
                            if header['name'] == 'To':
                                _to.append(header['value'].encode('utf8'))
                            else:
                                _to.append('')
                                #print header['value']

            else:
                print "Bad request to Gmail API service or there's no messages in your messages ID's list."
                return

        return messages_IDs, subjects, _dates, _from, _to
        
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        