"""
Config for the Qdrant Vector DB Client
"""

import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_CLIENT_LOG_PATH = os.getenv("QDRANT_CLIENT_LOG_PATH", "logs/qdrant_client.log")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
