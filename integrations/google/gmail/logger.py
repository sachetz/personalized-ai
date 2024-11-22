import logging
from config import LOG_FILE_PATH
import os

# Create the logs directory if it does not exist
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    return logging.getLogger(__name__)
