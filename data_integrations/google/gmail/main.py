# main.py

from auth import authenticate_gmail
from email_handler import list_emails, get_email_details
from utils import store_emails
from logger import setup_logger

def main():
    logger = setup_logger()
    logger.info('Starting Gmail Connector')
    
    # Authenticate and create Gmail service
    service = authenticate_gmail()
    
    # Define your search query
    query = 'newer_than:7d'  # Example query: emails from the last 7 days
    max_emails = 50  # Adjust as needed
    
    # List emails
    logger.info('Listing emails...')
    messages = list_emails(service, query=query, max_results=max_emails)
    logger.info(f'Found {len(messages)} emails.')
    
    # Fetch and parse each email
    emails_data = []
    for msg in messages:
        msg_id = msg['id']
        email_details = get_email_details(service, msg_id)
        if email_details:
            emails_data.append(email_details)
    
    # Store emails
    store_emails(emails_data, filename='emails.json')
    logger.info('Gmail Connector finished successfully')

if __name__ == '__main__':
    main()
