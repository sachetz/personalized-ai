import time
import random
import json
import logging

from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

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
                logger.warning(f'API error {error.resp.status}. Retrying in {sleep_time:.2f} seconds...')
                time.sleep(sleep_time)
            elif error.resp.status in [401, 403]:
                logger.error(f'Authentication error {error.resp.status}: {error}')
                raise error
            else:
                logger.error(f'Unexpected API error {error.resp.status}: {error}')
                raise error
    logger.error("Max retries exceeded")
    raise Exception("Max retries exceeded")

def store_emails(emails, filename='emails.json'):
    """
    Stores a list of email dictionaries into a JSON file.
    
    :param emails: List of email dictionaries
    :param filename: Destination JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(emails, f, ensure_ascii=False, indent=4)
        logger.info(f'Successfully stored {len(emails)} emails to {filename}')
    except Exception as e:
        logger.error(f'An error occurred while storing emails: {e}')