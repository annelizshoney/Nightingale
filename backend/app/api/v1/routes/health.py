from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():

    return {
        "success": True,
        "data": {
            "heartRate": 82,
            "temperature": 36.8,
            "oxygen": 97,
            "status": "Normal"
        }
    }