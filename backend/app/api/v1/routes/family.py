from fastapi import APIRouter

router = APIRouter(tags=["Family"])


@router.get("/family")
def family():

    return {
        "success": True,
        "data": [
            {
                "name": "John",
                "relation": "Son",
                "status": "Notified"
            }
        ]
    }