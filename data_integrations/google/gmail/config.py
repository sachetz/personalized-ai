# src/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', '.creds/credentials.json')
GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', '.creds/gmail_token.pickle')
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/gmail_connector.log')
