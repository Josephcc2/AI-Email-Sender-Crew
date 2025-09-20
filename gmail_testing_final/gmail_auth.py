import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle

# Scopes determine the level of access. 'modify' allows reading, sending, deleting.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None

    # Load token from pickle file if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, do login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def list_messages(service):
    # Only fetch emails with the INBOX label (exclude sent messages)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print('No messages found.')
    else:
        print('Recent message IDs:')
        for msg in messages:
            print(msg['id'])

if __name__ == '__main__':
    gmail_service = authenticate_gmail()
    list_messages(gmail_service)

def send_email(service, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    message = service.users().messages().send(userId='me', body=body).execute()
    print('Message Id:', message['id'])

def get_all_senders(service, max_results=50):
    senders = []

    # Fetch messages with the INBOX label only
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return senders

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From']).execute()
        headers = msg_data['payload'].get('headers', [])

        for header in headers:
            if header['name'] == 'From':
                senders.append(header['value'])
                break  # Only take the first "From" header

    return senders

def runGmail():
    gmail_service = authenticate_gmail()
    
    # List recent emails from inbox
    list_messages(gmail_service)

    gmail_service = authenticate_gmail()

    senders = get_all_senders(gmail_service)

    # Write to markdown file
    with open("Report.md", "w", encoding="utf-8") as f:
        for sender in senders:
            f.write(f"{sender}\n")
        #f.write(f"{senders[0]}\n")

    print(f"Wrote {len(senders)} senders to Report.md")

if __name__ == '__main__':
    runGmail()