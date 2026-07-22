from fastapi import APIRouter

router = APIRouter(tags=["Medication"])


@router.get("/medications")
def medications():

    return {
        "success": True,
        "data": [
            {
                "name": "Metformin",
                "time": "8:00 AM",
                "taken": True
            },
            {
                "name": "Aspirin",
                "time": "8:00 PM",
                "taken": False
            }
        ]
    }