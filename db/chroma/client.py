import chromadb

# Create the chroma client
# TODO: Add Auth
chroma_client = chromadb.HttpClient(host="localhost", port=8000)


def get_chroma_client():
    """
        Returns the chroma client
    """
    return chroma_client
