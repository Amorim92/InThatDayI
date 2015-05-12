from apiclient import errors


# Events IDs, status, summaries, creators, creation, start and end dates
events_IDs = []
status = []
summaries = []
creators = []
_created = []
_start = []
_end = []


def extract_events(service, token, before, after):

    try:
        # Result from Calendar API call
        events = service.events().list(calendarId = 'primary', orderBy = 'startTime', pageToken = token,
                                       showDeleted = True, singleEvents= True, timeZone = 'Lisbon',
                                       fields = 'items(creator(displayName),status,created,summary,location,start,end,id),nextPageToken').execute()


        # Append data of each event to the correspondent array
        # if events != None:
        #     if 'items' in events:
        try:
            # Event ID
            events_IDs = [item['id'] for item in events['items'] if after <= item['created'][:10] <= before]
            status = [item['status'] for item in events['items'] if after <= item['created'][:10] <= before]
            _created = [item['created'][:16].replace('T', ' ') for item in events['items'] if after <= item['created'][:10] <= before]
            summaries = [item['summary'].lower().encode('utf8') for item in events['items'] if after <= item['created'][:10] <= before]
            creators = [item['creator']['displayName'].encode('utf8') for item in events['items'] if after <= item['created'][:10] <= before]
            _start = [item['start']['dateTime'][:16].replace('T', ' ') for item in events['items'] if after <= item['created'][:10] <= before]
            _end = [item['end']['dateTime'][:16].replace('T', ' ') for item in events['items'] if after <= item['created'][:10] <= before]
                # for item in events['items']:
                #     if after <= item['created'][:10] <= before:
                #         # Event ID
                #         events_IDs = [item['id'] for item in events['items']]
                #         # Status
                #         status.append(item['status'])
                #         # Creation date
                #         _created.append(item['created'][:16].replace('T', ' '))
                #         # Summary
                #         summaries.append(item['summary'].lower().encode('utf8'))
                #         # Name of the creator
                #         creators.append(item['creator']['displayName'].encode('utf8'))
                #         # Start and end dates
                #         _start.append(item['start']['dateTime'][:16].replace('T', ' '))
                #         _end.append(item['end']['dateTime'][:16].replace('T', ' '))
                #     else:
                #         continue

            # Call function with page token
            if 'nextPageToken' in events:
                token = events['nextPageToken']
                extract_events(service, token, before, after)

        except:
            print "Bad request to Calendar API service or there's no events in your Google Calendar."
            return

        #print len(events_IDs), len(status), len(_created), len(summaries), len(creators), len(_start), len(_end)
        return events_IDs, status, summaries, creators, _created, _start, _end
    
    except errors.HttpError, error:
        print 'An error occurred during event extraction: %s' % error


# Clean function
def clean():
    try:
        # Events IDs, status, dates of creation, summaries, creators, start and end dates
        del events_IDs[:]
        del status[:]
        del _created[:]
        del summaries[:]
        del creators[:]
        del _start[:]
        del _end[:]
    except errors.HttpError, error:
        print 'Error cleaning: %s' % error