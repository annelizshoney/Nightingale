from qdrant_client import QdrantClient

from app.core.settings import settings


client = QdrantClient(
    url=settings.QDRANT_URL
)


COLLECTION_NAME = settings.QDRANT_COLLECTION


def get_qdrant_client():
    return client