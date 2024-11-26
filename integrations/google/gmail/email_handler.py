"""
Methods to interact with Gmail API
"""

import base64
from email import policy
from email.parser import BytesParser

from integrations.google.gmail.utils import robust_request
from integrations.google.gmail.config import GMAIL_LOG_FILE_PATH
from logger.logger import setup_logger

logger = setup_logger(GMAIL_LOG_FILE_PATH)

def list_emails(service, user_id="me", query="", max_results=100):
    """
    List email IDs matching the query.
    
    :param service: Authenticated Gmail service object
    :param user_id: User"s email address. "me" refers to the authenticated user
    :param query: Gmail search query (e.g., "is:unread", "from:someone@example.com")
    :param max_results: Maximum number of emails to retrieve
    :return: List of email IDs
    """

    try:
        response = robust_request(
            lambda: service.users()
                .messages()
                .list(userId=user_id, q=query, maxResults=max_results)
                .execute()
        )
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])

        # Handle pagination if necessary
        while "nextPageToken" in response and len(messages) < max_results:
            page_token = response["nextPageToken"]
            response = robust_request(
                lambda: service.users()
                    .messages()
                    .list(userId=user_id, q=query, pageToken=page_token, maxResults=max_results)
                    .execute()
                )
            if "messages" in response:
                messages.extend(response["messages"])
            logger.info("Retrieved %d emails so far", len(messages))

        logger.info("Total emails retrieved: %d", len(messages))
        return messages[:max_results]
    except Exception as e:
        logger.error("An error occurred while listing emails: %s", str(e))
        return []

def get_email_details(service, msg_id, user_id="me"):
    """
    Fetch and parse the email content.
    
    :param service: Authenticated Gmail service object
    :param msg_id: ID of the email to fetch
    :param user_id: User's email address. "me" refers to the authenticated user
    :return: Parsed email content as a dictionary
    """
    try:
        # Fetch the email in raw format
        message = robust_request(
            lambda: service.users()
                .messages()
                .get(userId=user_id, id=msg_id, format="raw")
                .execute()
        )
        msg_raw = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))

        # Parse the email using the email library
        mime_msg = BytesParser(policy=policy.default).parsebytes(msg_raw)

        # Extract headers
        headers = {header: mime_msg[header] for header in ["From", "To", "Subject", "Date"]}

        # Extract body (text/plain and text/html)
        body = ""
        html_body = ""
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get_content_disposition())
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body += part.get_content()
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    html_body += part.get_content()
        else:
            content_type = mime_msg.get_content_type()
            if content_type == "text/plain":
                body = mime_msg.get_content()
            elif content_type == "text/html":
                html_body = mime_msg.get_content()

        # Extract attachments (optional)
        attachments = []
        for part in mime_msg.iter_attachments():
            filename = part.get_filename()
            content = part.get_content()
            attachments.append({
                "filename": filename,
                "content_type": part.get_content_type(),
                "data": content  # This is raw binary data
            })

        email_data = {
            "id": message["id"],
            "threadId": message.get("threadId"),
            "labels": message.get("labelIds"),
            "snippet": message.get("snippet"),
            "headers": headers,
            "body": body,
            "html_body": html_body,
            "attachments": attachments
        }

        logger.info("Fetched email ID: %s", str(msg_id))
        return email_data
    except Exception as e:
        logger.error("An error occurred while fetching email %s: %s", str(msg_id), str(e))
        return {}
