import httpx
from config import settings

SEOUL_BASE = "http://ws.bus.go.kr/api/rest"
GYEONGGI_BASE = "http://apis.data.go.kr/6410000"


def _seoul_params(extra: dict) -> dict:
    return {"ServiceKey": settings.seoul_bus_api_key, "resultType": "json", **extra}


def _gyeonggi_params(extra: dict) -> dict:
    return {"serviceKey": settings.gyeonggi_bus_api_key, "format": "json", **extra}


def search_stations_seoul(query: str) -> list[dict]:
    resp = httpx.get(
        f"{SEOUL_BASE}/stationinfo/getStationByName",
        params=_seoul_params({"stSrch": query}),
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json().get("msgBody", {})
    items = body.get("itemList", [])
    if isinstance(items, dict):
        items = [items]
    return [
        {
            "station_id": item["stId"],
            "station_name": item["stNm"],
            "city": "seoul",
        }
        for item in items
    ]


def search_stations_gyeonggi(query: str) -> list[dict]:
    resp = httpx.get(
        f"{GYEONGGI_BASE}/busstationservice/getBusStationList",
        params=_gyeonggi_params({"stationName": query}),
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json().get("response", {}).get("msgBody", {})
    items = body.get("busStationList", [])
    if isinstance(items, dict):
        items = [items]
    return [
        {
            "station_id": item["stationId"],
            "station_name": item["stationName"],
            "city": "gyeonggi",
        }
        for item in items
    ]


def get_arrivals_seoul(station_id: str) -> list[dict]:
    resp = httpx.get(
        f"{SEOUL_BASE}/stationinfo/getStationByUid",
        params=_seoul_params({"arsId": station_id}),
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json().get("msgBody", {})
    items = body.get("itemList", [])
    if isinstance(items, dict):
        items = [items]
    return [
        {
            "route_name": item.get("rtNm", ""),
            "arrival_msg": item.get("arrmsg1", "정보 없음"),
            "arrival_msg2": item.get("arrmsg2", ""),
        }
        for item in items
    ]


def get_arrivals_gyeonggi(station_id: str) -> list[dict]:
    resp = httpx.get(
        f"{GYEONGGI_BASE}/busarrivalservice/getBusArrivalList",
        params=_gyeonggi_params({"stationId": station_id}),
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json().get("response", {}).get("msgBody", {})
    items = body.get("busArrivalList", [])
    if isinstance(items, dict):
        items = [items]
    return [
        {
            "route_name": item.get("routeName", ""),
            "arrival_msg": item.get("predictTime1", "정보 없음"),
            "arrival_msg2": item.get("predictTime2", ""),
        }
        for item in items
    ]
