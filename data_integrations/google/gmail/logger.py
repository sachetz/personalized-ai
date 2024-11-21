# src/logger.py

import logging
from config import LOG_FILE_PATH
import os

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    return logging.getLogger(__name__)
