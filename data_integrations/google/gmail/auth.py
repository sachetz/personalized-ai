# src/auth.py

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH
from logger import setup_logger

logger = setup_logger()

def authenticate_gmail():
    """
    Authenticate the user and return the Gmail service object.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    # Check if token.pickle exists (stores user's access and refresh tokens)
    if os.path.exists(GMAIL_TOKEN_PATH):
        with open(GMAIL_TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
            logger.info('Loaded credentials from token.pickle')
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info('Refreshed expired credentials')
            except Exception as e:
                logger.error(f'Error refreshing credentials: {e}')
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info('Performed new authentication flow')
            except Exception as e:
                logger.error(f'Error during authentication flow: {e}')
                raise e
        # Save the credentials for the next run
        with open(GMAIL_TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
            logger.info('Saved new credentials to token.pickle')
    
    # Build the Gmail service
    try:
        service = build('gmail', 'v1', credentials=creds)
        logger.info('Built Gmail service successfully')
    except Exception as e:
        logger.error(f'Error building Gmail service: {e}')
        raise e
    
    return service