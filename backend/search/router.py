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
    except Exception:
        errors.append("서울 API 조회에 실패했습니다.")

    try:
        results += search_stations_gyeonggi(q)
    except Exception:
        errors.append("경기 API 조회에 실패했습니다.")

    if not results and errors:
        raise HTTPException(status_code=502, detail="버스 정류장 검색에 실패했습니다. 잠시 후 다시 시도해주세요.")

    return {"results": results, "errors": errors}
