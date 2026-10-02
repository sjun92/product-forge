from fastapi import APIRouter, Depends, Query
from auth.dependencies import require_approved
from arrivals.cache import arrival_cache
from arrivals.public_api import get_arrivals_seoul, get_arrivals_gyeonggi
from models import User

router = APIRouter(prefix="/arrivals", tags=["arrivals"])


@router.get("")
def get_arrivals(
    station_id: str = Query(...),
    city: str = Query(...),   # 'seoul' | 'gyeonggi'
    user: User = Depends(require_approved),
):
    fetcher = get_arrivals_seoul if city == "seoul" else get_arrivals_gyeonggi

    try:
        data = arrival_cache.get(city, station_id, fetcher)
        return {"arrivals": data, "stale": False}
    except Exception as e:
        # 캐시에 이전 데이터가 있으면 반환 (stale fallback)
        key = f"{city}:{station_id}"
        entry = arrival_cache._store.get(key)
        if entry:
            return {"arrivals": entry["data"], "stale": True, "error": str(e)}
        return {"arrivals": [], "stale": True, "error": str(e)}
