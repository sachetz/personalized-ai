"""
Authentication for the Google API for Google Calendar Integration
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from integrations.google.calendar.config import (
    GOOGLE_CALENDAR_CREDENTIALS,
    GOOGLE_CALENDAR_TOKEN_PATH,
    GOOGLE_CALENDAR_LOG_FILE
)
from logger.logger import setup_logger

logger = setup_logger(GOOGLE_CALENDAR_LOG_FILE)

def authenticate_google_calendar(user_id: int):
    """
    Authenticate the user and return the Gmail service object.
    """

    scopes = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    token_path = GOOGLE_CALENDAR_TOKEN_PATH + str(user_id) + "_google_calendar_token.pickle"

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
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CALENDAR_CREDENTIALS, scopes)
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
        service = build("calendar", "v3", credentials=creds)
        logger.info("Built Google Calendar service successfully")
    except Exception as e:
        logger.error("Error building Google Calendar service: %s", str(e))
        raise e

    return service
