from integrations.google.gmail.fetch import fetch_emails
from integrations.google.gmail.utils import clean_emails
from db.mysql.utils import update_last_sync_at
from llm.openai.client import OpenAIClient
from db.qdrant.client import QdrantDBClient

openai_client = OpenAIClient()
qdrant_client = QdrantDBClient()


def sync(user_id: int, last_sync_at: int):
    emails, new_last_sync_at = fetch_emails(user_id, last_sync_at)
    cleaned_emails = clean_emails(emails)
    for email in cleaned_emails:
        embedding_vector = openai_client.get_text_embedding(email["body"])
        qdrant_client.insert_data(user_id, "emails", email, embedding_vector, False)
    update_last_sync_at(user_id, new_last_sync_at)
