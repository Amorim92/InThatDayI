from apiclient import errors


# Documents IDs, title, date of creation, creators
documents_IDs = []
titles = []
_created = []
owners = []


def extract_documents(service, query, token):

    try:
        # Result from Drive API call
        documents = service.files().list(corpus = 'DOMAIN', pageToken = token, q = query,
                                         fields = 'items(owners(displayName),id,description,createdDate,title),nextPageToken').execute()
        

        # Append data of each event to the correspondent array
        if documents != None:
            if 'items' in documents:
                for item in documents['items']:
                    # Document ID
                    documents_IDs.append(item['id'])
                    # Document title
                    titles.append(item['title'].encode('utf8'))
                    # Creation date
                    _created.append(item['createdDate'][:10] + ' ' + item['createdDate'][11:-8])
                    # Name of the owner
                    owners.append(item['owners'][0]['displayName'].encode('utf8'))


            # Call function with page token
            if 'nextPageToken' in documents:
                token = documents['nextPageToken']
                extract_documents(service, query, token)

        else:
            print "Bad request to Drive API service or there's no documents in your Google Drive."
            return

        return documents_IDs, titles, _created, owners

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        