"""
Implementation of the OpenAI LLM Client
"""

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from llm.openai.config import OPENAI_LOG_FILE_PATH
from logger.logger import setup_logger

load_dotenv()
logger = setup_logger(OPENAI_LOG_FILE_PATH)

class OpenAIClient:
    """
    OpenAI Client
    """

    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton class implementation.
        """

        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, model="text-embedding-3-small"):
        self._client = OpenAIEmbeddings(
            model=model
        )

    def get_text_embedding(self, text):
        """
        Converts a given text string into its embedding using OpenAI"s embedding model.

        :param text: The input text to embed.

        :return list: The embedding vector.
        """

        try:
            vector = self._client.embed_query(text)
            return vector
        except Exception as e:
            logger.info("An error occurred: %s", str(e))
            return None
