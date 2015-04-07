from apiclient import errors


# Events IDs, status, dates of creation, summaries, creators, start and end dates
events_IDs = []
status = []
_created = []
summaries = []
creators = []
_start = []
_end = []


def extract_events(service, query, token):

    try:
        # Result from Calendar API call
        events = service.events().list(calendarId = 'primary', orderBy = 'startTime', pageToken = token,
                                       q = query, showDeleted = True, singleEvents= True, timeZone = 'Lisbon',
                                       fields = 'items(creator(displayName),status,created,summary,location,start,end,id),nextPageToken').execute()


        # Append data of each event to the correspondent array
        if events != None:
            if 'items' in events:
                for item in events['items']:
                    # Event ID
                    events_IDs.append(item['id'])
                    # Status
                    status.append(item['status'])
                    # Creation date
                    _created.append(item['created'][:10] + ' ' + item['created'][11:-8])
                    # Summary
                    summaries.append(item['summary'].encode('utf8'))
                    # Name of the creator
                    creators.append(item['creator']['displayName'].encode('utf8'))
                    
                    # Start and end dates
                    if item['start']['dateTime'][-1] == '0' and item['end']['dateTime'][-1] == '0':
                        _start.append(item['start']['dateTime'][:10] + ' ' + item['start']['dateTime'][11:-9])
                        _end.append(item['end']['dateTime'][:10] + ' ' + item['end']['dateTime'][11:-9])
                    else:
                        _start.append(item['start']['dateTime'][:10] + ' ' + item['start']['dateTime'][11:-4])
                        _end.append(item['end']['dateTime'][:10] + ' ' + item['end']['dateTime'][11:-4])


            # Call function with page token
            if 'nextPageToken' in events:
                token = events['nextPageToken']
                extract_events(service, query, token)

        else:
            print "Bad request to Calendar API service or there's no events in your Google Calendar."
            return

        return events_IDs, status, _created, summaries, creators, _start, _end

    except errors.HttpError, error:
        print 'An error occurred: %s' % error