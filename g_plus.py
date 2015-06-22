from apiclient import errors


# Actors, publications,  and dates
activities_IDs = []
publications = []
actors = []
urls = []
_created = []


def extract_publications(service, token, before, after):

    try:
        # Result from Google+ API call
        activities = service.activities().list(userId = 'me', collection = 'public', pageToken = token,
                                               fields = 'items(url,published,object/attachments/displayName,actor/displayName,id),nextPageToken').execute()
        

        # Append data of each activity to the correspondent array
        if activities is not None:
            if 'items' in activities:
                for item in activities['items']:
                    if after <= item['published'][:10] <= before:
                        # Activity ID
                        activities_IDs.append(item['id'])
                        # Publication text
                        publications.append(item['object']['attachments'][0]['displayName'].lower().encode('utf8'))
                        # Actors
                        actors.append(item['actor']['displayName'].encode('utf8'))
                        # Url of the publication
                        urls.append(item['url'])
                        # Publication date
                        _created.append(item['published'][:16].replace('T', ' '))
                    else:
                        continue

            # Call function with page token
            if 'nextPageToken' in activities:
                token = activities['nextPageToken']
                extract_publications(service, token, before, after)

        else:
            print "Bad request to Google+ API service or there's no publications in your Google+."
            return

        # print len(activities_IDs), len(publications), len(actors), len(urls), len(_created)
        return activities_IDs, publications, actors, urls, _created

    except errors.HttpError, error:
        print 'An error occurred during publication extraction: %s' % error


# Clean function
def clean():
    try:
        # Events IDs, status, dates of creation, summaries, creators, start and end dates
        del activities_IDs[:]
        del publications[:]
        del actors[:]
        del urls[:]
        del _created[:]
    except errors.HttpError, error:
        print 'Error cleaning: %s' % error