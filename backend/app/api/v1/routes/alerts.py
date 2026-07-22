from fastapi import APIRouter

router = APIRouter(tags=["Alerts"])


@router.get("/alerts")
def alerts():

    return {
        "success": True,
        "data": [
            {
                "id": 1,
                "severity": "HIGH",
                "message": "Missed insulin dose"
            }
        ]
    }