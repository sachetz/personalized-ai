"""
Syncing new integrations
"""

from integrations.google.gmail.auth import authenticate_gmail
from integrations.google.gmail.email_handler import list_emails, get_email_details
from integrations.google.gmail.config import GMAIL_LOG_FILE_PATH
from logger.logger import setup_logger

def sync():
    """
    Method to authenticate account and fetch emails
    """

    logger = setup_logger(GMAIL_LOG_FILE_PATH)
    logger.info("Starting Gmail Connector")

    # Authenticate and create Gmail service
    service = authenticate_gmail()

    # Define the search query
    query = "newer_than:7d"
    max_emails = 50  # Adjust as needed

    # List emails
    logger.info("Listing emails...")
    messages = list_emails(service, query=query, max_results=max_emails)
    logger.info("Found %d emails.", len(messages))

    # Fetch and parse each email
    emails_data = []
    for msg in messages:
        msg_id = msg["id"]
        email_details = get_email_details(service, msg_id)
        if email_details:
            emails_data.append(email_details)

    logger.info("Gmail Connector finished successfully")
    return emails_data
