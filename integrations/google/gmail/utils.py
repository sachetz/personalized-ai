"""
Utils for Gmail Integration
"""

import time
import random
import logging
import html
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from dateutil import parser as date_parser
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
                logger.warning(
                    "API error %s. Retrying in %s seconds...",
                    str(error.resp.status),
                    f"{sleep_time:.2f}"
                )
                time.sleep(sleep_time)
            elif error.resp.status in [401, 403]:
                logger.error("Authentication error %s: %s", str(error.resp.status), str(error))
                raise error
            else:
                logger.error("Unexpected API error %s: %s", str(error.resp.status), str(error))
                raise error
    logger.error("Max retries exceeded")
    raise TimeoutError("Max retries exceeded")

def clean_emails(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans up a list of email dictionaries by extracting relevant information,
    decoding HTML entities, stripping HTML tags, and converting dates.

    Args:
        emails (List[Dict[str, Any]]): List of email data as dictionaries.

    Returns:
        List[Dict[str, Any]]: List of cleaned email data.
    """
    cleaned_emails = []
    
    for email in emails:
        cleaned_email = {}
        
        # Basic Fields
        cleaned_email['id'] = email.get('id')
        cleaned_email['threadId'] = email.get('threadId')
        cleaned_email['labels'] = email.get('labels', [])
        cleaned_email['snippet'] = html.unescape(email.get('snippet', ''))
        
        # Headers
        headers = email.get('headers', {})
        cleaned_email['from'] = headers.get('From', '')
        cleaned_email['to'] = headers.get('To', '')
        cleaned_email['subject'] = headers.get('Subject', '')
        
        # Date Parsing
        date_str = headers.get('Date', '')
        try:
            # Using dateutil for flexible parsing
            cleaned_email['date'] = date_parser.parse(date_str)
        except (ValueError, TypeError):
            # If parsing fails, set date to None
            cleaned_email['date'] = None
        
        # Body Processing
        body_text = email.get('body', '')
        html_body = email.get('html_body', '')
        
        if html_body:
            # Parse HTML and extract plain text
            soup = BeautifulSoup(html_body, 'html.parser')
            # Get text with proper line breaks
            plain_text = soup.get_text(separator='\n')
            cleaned_email['body'] = html.unescape(plain_text)
        else:
            # If no HTML body, use the plain text body
            cleaned_email['body'] = html.unescape(body_text)
        
        # Attachments (retain as-is or process further)
        attachments = email.get('attachments', [])
        cleaned_email['attachments'] = attachments  # Modify as needed
        
        # Append the cleaned email to the list
        cleaned_emails.append(cleaned_email)
    
    return cleaned_emails