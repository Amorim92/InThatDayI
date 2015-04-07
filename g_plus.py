import sys
from apiclient import errors


# Actors, publications,  and dates
actors = []
urls = []
pubs = []
summaries = []
_start = []
_end = []


def extract_publications(service, token):

    try:
        # Result from Gmail API call
        events = service.events().list(calendarId = 'primary', orderBy = 'startTime', pageToken = token,
                                       showDeleted = True, singleEvents= True, timeZone = 'Lisbon',
                                       fields = 'items(creator(displayName),status,created,summary,location,start,end),nextPageToken').execute()
        if events != None:
            # Append each event to events
            if 'items' in events:
                for item in events['items']:
                    status.append(item['status'])
                    _created.append(item['created'][:10] + ' ' + item['created'][11:-8])
                    summaries.append(item['summary'].lower())
                    creators.append(item['creator']['displayName'].lower())
                    
                    if item['start']['dateTime'][-1] == '0' and item['end']['dateTime'][-1] == '0':
                        _start.append(item['start']['dateTime'][:10] + ' ' + item['start']['dateTime'][11:-9])
                        _end.append(item['end']['dateTime'][:10] + ' ' + item['end']['dateTime'][11:-9])
                    else:
                        _start.append(item['start']['dateTime'][:10] + ' ' + item['start']['dateTime'][11:-4])
                        _end.append(item['end']['dateTime'][:10] + ' ' + item['end']['dateTime'][11:-4])

            while 'nextPageToken' in events:
                token = events['nextPageToken']

                # Call function with page token
                extract_events(service, token)

            #print status
            #print _created
            #print summaries
            #for x in creators:
            #print creators
            #print _start
            #print _end

            return status, _created, summaries, creators, _start, _end

        else:
            print "Bad request to Gmail API service."

    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        