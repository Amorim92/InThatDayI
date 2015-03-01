from apiclient.discovery import build
from apiclient import errors

"""Build a Drive service object.
Args:
    credentials: OAuth 2.0 credentials.
Returns:
    Drive service object.
"""
def build_service(credentials):
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('drive', 'v2', http = http)


"""Print a file's metadata.
Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
"""
def print_file(service, file_id):
    try:
        file = service.files().get(fileId=file_id).execute()
        print 'Title: %s' % file['title']
        print 'Description: %s' % file['description']
        print 'MIME type: %s' % file['mimeType']
    except errors.HttpError, error:
        if error.resp.status == 401:
            # Credentials have been revoked.
            # TODO: Redirect the user to the authorization URL.
            raise NotImplementedError()