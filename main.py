from __future__ import print_function
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    print("Enter your LASID:")
    user_lasid = input()
    if '@' in user_lasid: user_lasid.split('@')[0]

    print(user_lasid)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(user_lasid + '_token.json'):
        creds = Credentials.from_authorized_user_file(user_lasid + '_token.json', SCOPES)
    # If there are no (valid) credential available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        print(creds)
        service = build('gmail', 'v1', credentials=creds)
        user_profile = service.users().getProfile(userId='me').execute()
        user_lasid = user_profile['emailAddress'].split('@')[0]
        print(user_lasid)
        user = {}
        user[user_lasid] = json.loads(creds.to_json())
        print(user)
        print(creds.to_json())
        with open(user_lasid + '_token.json', 'w') as token:
            token.write(json.dumps(user))

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()