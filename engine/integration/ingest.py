"""
Something something
"""

from dotenv import load_dotenv
from openai import OpenAI
from config import OPENAI_LOG_FILE_PATH
from logger.logger import setup_logger

load_dotenv()

client = OpenAI()
logger = setup_logger(OPENAI_LOG_FILE_PATH)

def get_text_embedding(text, model="text-embedding-3-small"):
    """
    Converts a given text string into its embedding using OpenAI"s embedding model.

    :param text: The input text to embed.
    :param model (optional): The embedding model to use.

    :return list: The embedding vector.
    """

    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        logger.info("An error occurred: %s", str(e))
        return None



if __name__ == "__main__":
    embedding = get_text_embedding("OpenAI provides powerful language models.")

    if embedding:
        print(embedding)
    else:
        print("Failed to retrieve embedding.")
