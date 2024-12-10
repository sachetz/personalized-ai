"""
Authentication for the Google API for Gmail Integration
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from integrations.google.gmail.config import (
    GMAIL_CREDENTIALS,
    GMAIL_TOKEN_PATH,
    GMAIL_LOG_FILE
)
from logger.logger import setup_logger

logger = setup_logger(GMAIL_LOG_FILE)

def authenticate_gmail(user_id: int):
    """
    Authenticate the user and return the Gmail service object.
    """

    scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    token_path = GMAIL_TOKEN_PATH + str(user_id) + "_gmail_token.pickle"

    # Check if token.pickle exists (stores user"s access and refresh tokens)
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
            logger.info("Loaded credentials from token.pickle")

    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Refreshed expired credentials")
            except Exception as e:
                logger.error("Error refreshing credentials: %s", str(e))
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS, scopes)
                creds = flow.run_local_server(port=0)
                logger.info("Performed new authentication flow")
            except Exception as e:
                logger.error("Error during authentication flow: %s", str(e))
                raise e
        # Save the credentials for the next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)
            logger.info("Saved new credentials to token.pickle")

    # Build the Gmail service
    try:
        service = build("gmail", "v1", credentials=creds)
        logger.info("Built Gmail service successfully")
    except Exception as e:
        logger.error("Error building Gmail service: %s", str(e))
        raise e

    return service
