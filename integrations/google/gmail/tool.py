from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from typing import Annotated
from db.qdrant.client import QdrantDBClient
from llm.openai.client import OpenAIClient

qdrant_client = QdrantDBClient()
openai_client = OpenAIClient()

@tool(parse_docstring=True)
def email_search_tool(
    query: str,
    config: RunnableConfig,
):
    """Use this to search for information and details specific to the user.
    This tool searches for the information about the user from their emails.
    This is visible to the user.
    
    Args:
        query: The query from the user
    """

    try:
        user_id = config.get("configurable", {}).get("user_id")
        embeddings = openai_client.get_text_embedding(query)
        return qdrant_client.search(user_id, "emails", embeddings)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
