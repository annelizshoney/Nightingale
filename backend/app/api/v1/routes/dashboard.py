from fastapi import APIRouter

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
def dashboard():

    return {
        "success": True,
        "message": "Dashboard fetched successfully",
        "data": {
            "elder": {
                "name": "Mary Johnson",
                "age": 74
            },
            "health": {
                "heartRate": 78,
                "bloodPressure": "120/80",
                "oxygen": 98
            },
            "medication": {
                "nextDose": "8:00 PM",
                "missedToday": False
            },
            "risk": {
                "level": "LOW",
                "score": 12
            }
        }
    }