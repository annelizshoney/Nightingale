from fastapi import APIRouter

router = APIRouter(tags=["Memory"])


@router.get("/memory")
def memory():

    return {
        "success": True,
        "data": [
            {
                "date": "2026-07-20",
                "event": "Visited Doctor"
            },
            {
                "date": "2026-07-21",
                "event": "Missed Evening Medication"
            }
        ]
    }