"""
Integration Engine Env Config
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables
OPENAI_LOG_FILE_PATH = os.getenv("OPENAI_LOG_FILE_PATH", "logs/openai_client.log")
