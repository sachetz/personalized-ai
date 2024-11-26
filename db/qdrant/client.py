"""
Implementation of the Qdrant Vector DB Client
"""

import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    KeywordIndexParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)


class QdrantDBClient:
    """
    Qdrant Vector DB Client
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

    def __init__(self):
        """
        Initialise a Qdrant Client.
        """

        if not self._client:
            self._client = QdrantClient(url="http://localhost:6333")

    def _create_index_for_collection(self, collection_name):
        """
        Index the collection for individual users.

        :param collection_name: Name of the collection to create payload index for
        """

        self._client.create_payload_index(
            collection_name=collection_name,
            field_name="user_id",
            field_schema=KeywordIndexParams(
                type="keyword",
                is_tenant=True
            )
        )

    def create_collection(self, collection_name, size=1536, distance=Distance.DOT):
        """
        Creates a collection, and indexes it for user_id
        
        :param collection_name: Name of the collection to create
        :param size (optional): Size of the embedding vectors,
            default is 1536 (OpenAI's text-embedding-3-small)
        :param distance (optional): Distance metric to use, default is dot product
        """

        try:
            # Create a collection
            self._client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=size, distance=distance),
                hnsw_config=HnswConfigDiff(payload_m=42, m=0)
            )
            self._create_index_for_collection(collection_name=collection_name)
        except Exception as e:
            raise e

    def insert_data(self, user_id, collection_name, data, data_vector, wait=True):
        """
        Insert the data into the collection

        :param user_id: User ID, used to partition the collection
        :param collection_name: Name of the collection to insert data into
        :param data: The data to add as payload
        :param data_vector: The embedding vector for the data
        :param wait (optional): Whether the client should wait for insert to complete
        """

        try:
            point_id = uuid.uuid4()
            self._client.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id=point_id,
                        payload={"user_id": user_id, "data": data},
                        vector=data_vector
                    )
                ],
                wait=wait
            )
        except Exception as e:
            raise e

    def search(self, user_id, collection_name, query_vector, limit=10):
        """
        Search the collection for the user_id and the query vector
        
        :param user_id: User ID, used to check the correct partition in the collection
        :param collection_name: Name of the collection to search
        :param query_vector: Embedding vector for the query
        :param limit (optional): Number of points to retrieve from the db

        :return records: Top matching records 
        """

        records = self._client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(key="user_id", match=MatchValue(value=user_id))
                ]
            ),
            limit=limit
        )

        return records
