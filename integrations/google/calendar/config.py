"""
Google Calendar Integration Env Config
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_PATH", ".creds/credentials.json")
GOOGLE_CALENDAR_TOKEN_PATH = os.getenv("GOOGLE_CALENDAR_TOKEN_PATH", ".creds/")
GOOGLE_CALENDAR_LOG_FILE = os.getenv("GOOGLE_CALENDAR_LOG_FILE_PATH", "logs/google_calendar_connector.log")
