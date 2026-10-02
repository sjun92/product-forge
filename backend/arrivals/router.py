from typing import Literal
from fastapi import APIRouter, Depends, Query
from auth.dependencies import require_approved
from arrivals.cache import arrival_cache
from arrivals.public_api import get_arrivals_seoul, get_arrivals_gyeonggi
from models import User

router = APIRouter(prefix="/arrivals", tags=["arrivals"])


@router.get("")
def get_arrivals(
    station_id: str = Query(...),
    city: Literal["seoul", "gyeonggi"] = Query(...),
    user: User = Depends(require_approved),
):
    fetcher = get_arrivals_seoul if city == "seoul" else get_arrivals_gyeonggi

    try:
        data = arrival_cache.get(city, station_id, fetcher)
        return {"arrivals": data, "stale": False}
    except Exception as e:
        stale_data = arrival_cache.get_stale(city, station_id)
        if stale_data is not None:
            return {"arrivals": stale_data, "stale": True, "error": str(e)}
        return {"arrivals": [], "stale": True, "error": str(e)}
