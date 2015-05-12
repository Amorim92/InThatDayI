from apiclient import errors


# Messages IDs, subjects, from, to and dates
# messages_IDs = []
subjects = []
_from = [] 
_to = []
_dates = []


def extract_mails(service, query, token):

    try:
        # Messages IDs
        messages_IDs = []

        # Result from Gmail API call
        mails = service.users().messages().list(userId = 'me', q = query, pageToken = token,
                                                fields = 'messages(id),nextPageToken').execute()


        # Append the ID of each message to messages_IDs
        # if mails is not None:
        #     if 'messages' in mails:
        try:
            # for message in mails['messages']:
                # Message ID
            messages_IDs = [message['id'] for message in mails['messages']]

            # Call function with page token
            while 'nextPageToken' in mails:
                token = mails['nextPageToken']
                # Result from Gmail API call
                mails = service.users().messages().list(userId = 'me', q = query, pageToken = token,
                                                        fields = 'messages(id),nextPageToken').execute()
                # extract_mails(service, query, token)
                # print 'acabei'
                messages_IDs = [message['id'] for message in mails['messages']]

        except:
            print "Bad request to Gmail API service or there's no e-mails in your Gmail Account."
            return


        # Get data of each message ID
        for id in messages_IDs:
            # Result from Gmail API call
            messages = service.users().messages().get(userId = 'me', id = id, format = 'metadata',
                                                      metadataHeaders = ['From', 'To', 'Subject', 'Date'],
                                                      fields = 'payload').execute()


            # Append data of each message to the correspondent array
            # if messages is not None:
            #     if 'payload' in messages:
            #         if 'headers' in messages['payload']:
            try:
                # print id
                subjects = [header['value'].encode('utf8') for header in messages['payload']['headers'] if header['name'] == 'Subject']
                # for header in messages['payload']['headers']:
                #     # Subject
                #     # subjects = []
                #     # if header['name'] == 'Subject':

                #     # from
                #     if header['name'] == 'From':
                #         _from.append(header['value'].encode('utf8'))

                #     # to
                #     if header['name'] == 'To':
                #         _to.append(header['value'].encode('utf8'))

                #     # date
                #     if header['name'] == 'Date':
                #         if header['value'][1] == ' ':
                #             _dates.append('0' + header['value'][:16])
                #         elif not header['value'][1].isalpha():
                #             _dates.append(header['value'][:17])
                #         elif header['value'][0].isalpha() and header['value'][6] == ' ':
                #             _dates.append('0' + header['value'][5:21])
                #         else:
                #             _dates.append(header['value'][5:22])

            except:
                print "Bad request to Gmail API service or there's no messages in your messages ID's list."
                return

        print len(messages_IDs), len(subjects), len(_from), len(_to), len(_dates)
        return messages_IDs, subjects, _from, _to, _dates
        
    except errors.HttpError, error:
        print 'An error occurred during mail extraction: %s' % error


# Clean function
def clean():
    try:
        # Documents IDs, title, date of creation, creators
        # del messages_IDs[:]
        del subjects[:]
        del _from[:]
        del _to[:]
        del _dates[:]
    except errors.HttpError, error:
        print 'Error cleaning: %s' % error