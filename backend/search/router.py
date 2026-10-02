from fastapi import APIRouter, Depends, HTTPException, Query
from auth.dependencies import require_approved
from arrivals.public_api import search_stations_seoul, search_stations_gyeonggi
from models import User

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/stations")
def search_stations(
    q: str = Query(min_length=1),
    user: User = Depends(require_approved),
):
    results = []
    errors = []

    try:
        results += search_stations_seoul(q)
    except Exception as e:
        errors.append(f"서울 API 오류: {e}")

    try:
        results += search_stations_gyeonggi(q)
    except Exception as e:
        errors.append(f"경기 API 오류: {e}")

    if not results and errors:
        raise HTTPException(status_code=502, detail="; ".join(errors))

    return {"results": results, "errors": errors}
