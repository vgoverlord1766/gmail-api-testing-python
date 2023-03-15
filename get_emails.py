import authorization
from googleapiclient.discovery import build
import time

start = time.time()
# print("Enter your LASID:")
# user_input = input()
user_input = '201226051'
credentials = authorization.get_credentials(user_input)

service = build('gmail', 'v1', credentials=credentials)
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

result = service.users().messages().list(userId='me', maxResults=50).execute()
message_ids = result.get('messages')


messages = []
for message_id in message_ids:
    message = {}
    # Get the message from its id
    message_content = service.users().messages().get(userId='me', id=message_id['id']).execute()

    # Get value of 'payload' from dictionary 'txt'
    payload = message_content['payload']
    headers = payload['headers']
    message['snippet'] = message_content['snippet']
    # Look for Subject and Sender Email in the headers
    for header in headers:
        if header['name'] == 'Subject':
            message['subject'] = header['value']
        if header['name'] == 'From':
            message['sender'] = header['value']
        if header['name'] == 'Date':
            message['date'] = header['value']

    messages.append(message)

end = time.time()


print("The time of execution of above program is :",
      (end - start), "s")

print(messages[8])