from db.chroma import client

chroma_client = client.get_chroma_client()
chroma_client.list_collections()
