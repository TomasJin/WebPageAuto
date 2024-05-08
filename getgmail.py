import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import re

def getgmail(proxy_host, proxy_port,  fakeaddress, num):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists(str(num)+'//token.json'):
        creds = Credentials.from_authorized_user_file(str(num)+'//token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # os.environ['HTTP_PROXY'] = f'https://{proxy_host}:{proxy_port}'
            # os.environ['HTTPS_PROXY'] = f'https://{proxy_host}:{proxy_port}'
            flow = InstalledAppFlow.from_client_secrets_file(
                str(num)+'//credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(str(num)+'//token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # os.environ['HTTP_PROXY'] = f'https://{proxy_host}:{proxy_port}'
        # os.environ['HTTPS_PROXY'] = f'https://{proxy_host}:{proxy_port}'
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q='subject:"Verify your email address" to:' + fakeaddress, maxResults=10).execute()
        if 'messages' in results:
            first_message = results['messages'][0]
            message_id = first_message['id']
            message = service.users().messages().get(userId='me', id=message_id).execute()

            # Extract the raw HTML content from the message
            payload = message['payload']

            # Iterate over the parts of the payload
            for part in payload['parts']:
                # Check if the part is of type 'text/html'
                if part['mimeType'] == 'text/html':
                    # Extract the data from the part
                    data = part['body']['data']
                    # Decode the data from base64
                    decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')

                    # Use regular expressions to find the verification link
                    match = re.search(r'href="(https://www.upwork.com/nx/signup/verify-email/.*?)"', decoded_data)
                    if match:
                        verification_link = match.group(1)
                        break

            # Print the verification link
            print(verification_link)

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f'An error occurred: {error}')

    return verification_link
