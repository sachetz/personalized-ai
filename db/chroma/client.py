import chromadb

chroma_client = None

class ChromaClient:
    def __init__(self):
        # TODO: Add Auth
        self._chroma_client = chromadb.HttpClient(host="localhost", port=8000)


def get_chroma_client():
    if chroma_client is None:
        chroma_client = ChromaClient()
    return chroma_client
