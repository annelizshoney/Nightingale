from app.qdrant.client import (
    client,
    COLLECTION_NAME
)

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


VECTOR_SIZE = 384


def initialize_collection():

    collections = client.get_collections().collections

    existing = [
        c.name for c in collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )


def create_dummy_vector():

    return [0.0] * VECTOR_SIZE


def add_memory(
    memory_id: int,
    text: str
):

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=[

            PointStruct(

                id=memory_id,

                vector=create_dummy_vector(),

                payload={
                    "text": text
                }

            )

        ]

    )


def search_memory(query: str):

    result = client.search(

        collection_name=COLLECTION_NAME,

        query_vector=create_dummy_vector(),

        limit=5

    )

    return [
        item.payload
        for item in result
    ]