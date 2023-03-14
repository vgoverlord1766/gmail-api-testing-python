import get_user_credentials
from googleapiclient.discovery import build

print("Enter your LASID:")
user_input = input()

credentials = get_user_credentials.get_user_credentials(user_input)

service = build('gmail', 'v1', credentials=credentials)
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

if not labels:
    print('No labels found.')
print('Labels:')
for label in labels:
    print(label['name'])
