import os
import pickle
import base64
import json
import time
import random
import logging
import dotenv

from email import policy
from email.parser import BytesParser

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    filename='logs/gmail_connector.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def authenticate_gmail():
    """
    Authenticate the user and return the Gmail service object.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    token_pickle = '.creds/gmail_token.pickle'
    credentials_json = os.getenv('GMAIL_CREDENTIALS_PATH')  # Ensure this file exists

    # Check if token.pickle exists (stores user's access and refresh tokens)
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
            logging.info('Loaded credentials from token.pickle')
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logging.info('Refreshed expired credentials')
            except Exception as e:
                logging.error(f'Error refreshing credentials: {e}')
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info('Performed new authentication flow')
            except Exception as e:
                logging.error(f'Error during authentication flow: {e}')
                raise e
        # Save the credentials for the next run
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)
            logging.info('Saved new credentials to token.pickle')
    
    # Build the Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        logging.info('Built Gmail service successfully')
    except Exception as e:
        logging.error(f'Error building Gmail service: {e}')
        raise e
    
    return service

def robust_request(request_func, max_retries=5):
    """
    Executes a Gmail API request with exponential backoff on failure.
    
    :param request_func: Function that makes the API request
    :param max_retries: Maximum number of retries
    :return: Result of the API request
    """
    for attempt in range(max_retries):
        try:
            return request_func()
        except HttpError as error:
            if error.resp.status in [429, 500, 503]:
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                logging.warning(f'API error {error.resp.status}. Retrying in {sleep_time:.2f} seconds...')
                time.sleep(sleep_time)
            elif error.resp.status in [401, 403]:
                logging.error(f'Authentication error {error.resp.status}: {error}')
                raise error
            else:
                logging.error(f'Unexpected API error {error.resp.status}: {error}')
                raise error
    logging.error("Max retries exceeded")
    raise Exception("Max retries exceeded")

def list_emails(service, user_id='me', query='', max_results=100):
    """
    List email IDs matching the query.
    
    :param service: Authenticated Gmail service object
    :param user_id: User's email address. 'me' refers to the authenticated user
    :param query: Gmail search query (e.g., 'is:unread', 'from:someone@example.com')
    :param max_results: Maximum number of emails to retrieve
    :return: List of email IDs
    """
    try:
        response = robust_request(lambda: service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute())
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        
        # Handle pagination if necessary
        while 'nextPageToken' in response and len(messages) < max_results:
            page_token = response['nextPageToken']
            response = robust_request(lambda: service.users().messages().list(userId=user_id, q=query, pageToken=page_token, maxResults=max_results).execute())
            if 'messages' in response:
                messages.extend(response['messages'])
            logging.info(f'Retrieved {len(messages)} emails so far')
        
        logging.info(f'Total emails retrieved: {len(messages)}')
        return messages[:max_results]
    except Exception as e:
        logging.error(f'An error occurred while listing emails: {e}')
        return []

def get_email_details(service, msg_id, user_id='me'):
    """
    Fetch and parse the email content.
    
    :param service: Authenticated Gmail service object
    :param msg_id: ID of the email to fetch
    :param user_id: User's email address. 'me' refers to the authenticated user
    :return: Parsed email content as a dictionary
    """
    try:
        # Fetch the email in raw format
        message = robust_request(lambda: service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute())
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        
        # Parse the email using the email library
        mime_msg = BytesParser(policy=policy.default).parsebytes(msg_raw)
        
        # Extract headers
        headers = {header: mime_msg[header] for header in ['From', 'To', 'Subject', 'Date']}
        
        # Extract body (text/plain and text/html)
        body = ''
        html_body = ''
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get_content_disposition())
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    body += part.get_content()
                elif content_type == 'text/html' and 'attachment' not in content_disposition:
                    html_body += part.get_content()
        else:
            content_type = mime_msg.get_content_type()
            if content_type == 'text/plain':
                body = mime_msg.get_content()
            elif content_type == 'text/html':
                html_body = mime_msg.get_content()
        
        # Extract attachments (optional)
        attachments = []
        for part in mime_msg.iter_attachments():
            filename = part.get_filename()
            content = part.get_content()
            attachments.append({
                'filename': filename,
                'content_type': part.get_content_type(),
                'data': content  # This is raw binary data
            })
        
        email_data = {
            'id': message['id'],
            'threadId': message.get('threadId'),
            'labels': message.get('labelIds'),
            'snippet': message.get('snippet'),
            'headers': headers,
            'body': body,
            'html_body': html_body,
            'attachments': attachments
        }
        
        logging.info(f'Fetched email ID: {msg_id}')
        return email_data
    except Exception as e:
        logging.error(f'An error occurred while fetching email {msg_id}: {e}')
        return {}

def store_emails(emails, filename='emails.json'):
    """
    Stores a list of email dictionaries into a JSON file.
    
    :param emails: List of email dictionaries
    :param filename: Destination JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(emails, f, ensure_ascii=False, indent=4)
        logging.info(f'Successfully stored {len(emails)} emails to {filename}')
    except Exception as e:
        logging.error(f'An error occurred while storing emails: {e}')

def main():
    logging.info('Starting Gmail Connector')
    
    # Authenticate and create Gmail service
    service = authenticate_gmail()
    
    # Define your search query
    query = 'newer_than:7d'  # Example query: emails from the last 7 days
    max_emails = 50  # Adjust as needed
    
    # List emails
    logging.info('Listing emails...')
    messages = list_emails(service, query=query, max_results=max_emails)
    logging.info(f'Found {len(messages)} emails.')
    
    # Fetch and parse each email
    emails_data = []
    for msg in messages:
        msg_id = msg['id']
        email_details = get_email_details(service, msg_id)
        if email_details:
            emails_data.append(email_details)
    
    # Store emails
    store_emails(emails_data, filename='emails.json')
    logging.info('Gmail Connector finished successfully')

if __name__ == '__main__':
    main()
