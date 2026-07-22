from dataclasses import dataclass

from qdrant_client.models import Distance

from app.core.settings import settings


@dataclass(frozen=True, slots=True)
class QdrantConfig:
    url: str
    api_key: str | None
    collection_name: str
    prefer_grpc: bool
    vector_size: int
    search_limit: int
    embedding_model_name: str
    distance: Distance = Distance.COSINE


def get_qdrant_config() -> QdrantConfig:
    return QdrantConfig(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        prefer_grpc=settings.QDRANT_PREFER_GRPC,
        vector_size=settings.QDRANT_VECTOR_SIZE,
        search_limit=settings.QDRANT_SEARCH_LIMIT,
        embedding_model_name=settings.QDRANT_EMBEDDING_MODEL,
    )
