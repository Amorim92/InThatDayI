import httplib2

from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.tools import run

def authenticate():
    # Path to client_secret file
    CLIENT_SECRET_FILE = 'C:\client_secret.json'
    REDIRECT_URI = 'http://localhost:8080/'
    # Google scopes used
    OAUTH_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
                    'https://www.googleapis.com/auth/drive.readonly',
                    'https://www.googleapis.com/auth/gmail.readonly',
                    'https://www.googleapis.com/auth/plus.login',
                    'https://www.googleapis.com/auth/plus.me'
    ]

    # Location of the credentials storage file
    STORAGE = Storage('credentials.storage')

    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope = ' '.join(OAUTH_SCOPES))
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()

    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http = http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    services = build_services(http)
    return services


def build_services(http):
    calendar = build('calendar', 'v3', http = http)
    drive = build('drive', 'v2', http = http)
    gmail = build('gmail', 'v1', http = http)
    plus = build('plus', 'v1', http = http)
    return calendar, drive, gmail, plus
