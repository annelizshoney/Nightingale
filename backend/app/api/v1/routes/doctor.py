from fastapi import APIRouter

router = APIRouter(tags=["Doctor"])


@router.get("/doctor-summary")
def doctor_summary():

    return {
        "success": True,
        "data": {
            "summary": "Patient has stable vitals with one missed medication this week.",
            "risk": "Medium"
        }
    }