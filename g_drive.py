from apiclient import errors


# Documents IDs, title, date of creation, owners
documents_IDs = []
titles = []
_created = []
owners = []


def extract_documents(service, token, before, after):

    try:
        # Result from Drive API call
        documents = service.files().list(corpus = 'DOMAIN', pageToken = token,
                                         fields = 'items(owners(displayName),id,createdDate,title),nextPageToken').execute()
        

        # Append data of each document to the correspondent array
        if documents != None:
            if 'items' in documents:
                for item in documents['items']:
                    if after <= item['createdDate'][:10] <= before:
                        # Document ID
                        documents_IDs.append(item['id'])
                        # Document title
                        titles.append(item['title'].encode('utf8'))
                        # Creation date
                        _created.append(item['createdDate'][:16])
                        # Name of the owner
                        owners.append(item['owners'][0]['displayName'].encode('utf8'))
                    else:
                        continue

            # Call function with page token
            if 'nextPageToken' in documents:
                token = documents['nextPageToken']
                extract_documents(service, token, before, after)

        else:
            print "Bad request to Drive API service or there's no documents in your Google Drive."
            return

        # print len(documents_IDs), len(titles), len(_created), len(owners)
        return documents_IDs,titles, _created, owners

    except errors.HttpError, error:
        print 'An error occurred during document extraction: %s' % error

 
# Clean function
def clean():
    try:
        # Documents IDs, title, date of creation, creators
        del documents_IDs[:]
        del titles[:]
        del _created[:]
        del owners[:]
    except errors.HttpError, error:
        print 'Error cleaning: %s' % error