from __future__ import print_function
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.events.readonly',
          'https://www.googleapis.com/auth/tasks']


def is_user_authorized(user_lasid):
    with open('token.json', 'r') as token_file:
        return user_lasid in json.load(token_file)


def get_user_credentials(user_lasid):
    if is_user_authorized(user_lasid):
        with open('token.json', 'r') as token_file:
            user_credentials_json = json.load(token_file)[user_lasid]
        user_credentials = Credentials.from_authorized_user_info(user_credentials_json)
        return user_credentials
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'r') as token_file:
            data = json.loads(token_file.read())
            users = data
            print(users)
        users[user_lasid] = json.loads(credentials.to_json())
        with open('token.json', 'w') as token_file:
            token_file.write(json.dumps(users))


