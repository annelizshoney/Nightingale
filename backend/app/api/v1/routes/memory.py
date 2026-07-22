from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.dependencies import get_memory_service
from app.qdrant.memory_service import MemoryService
from app.schemas.memory import MemoryCreateRequest, MemoryItem, MemorySearchResponse

router = APIRouter(tags=["Memory"])


@router.post(
    "/memory",
    response_model=MemoryItem,
    status_code=status.HTTP_201_CREATED,
)
def create_memory(
    payload: MemoryCreateRequest,
    memory_service: MemoryService = Depends(get_memory_service),
) -> MemoryItem:
    return MemoryItem(**memory_service.store_memory(payload.text, payload.metadata))


@router.get(
    "/memory/search",
    response_model=MemorySearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_memory(
    query: str,
    memory_service: MemoryService = Depends(get_memory_service),
) -> MemorySearchResponse:
    return MemorySearchResponse(
        items=[MemoryItem(**item) for item in memory_service.search_memory(query)]
    )


@router.delete(
    "/memory/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_memory(
    memory_id: str,
    memory_service: MemoryService = Depends(get_memory_service),
) -> Response:
    if not memory_service.delete_memory(memory_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)