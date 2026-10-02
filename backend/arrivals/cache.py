import time
from typing import Callable


class ArrivalCache:
    def __init__(self, ttl_seconds: int = 30):
        self._ttl = ttl_seconds
        self._store: dict[str, dict] = {}

    def _key(self, city: str, station_id: str) -> str:
        return f"{city}:{station_id}"

    def get(self, city: str, station_id: str, fetcher: Callable) -> list[dict]:
        key = self._key(city, station_id)
        entry = self._store.get(key)
        now = time.time()

        if entry and entry["expires_at"] > now:
            return entry["data"]

        data = fetcher(station_id)
        self._store[key] = {"data": data, "expires_at": now + self._ttl}
        return data

    def get_stale(self, city: str, station_id: str) -> list[dict] | None:
        """캐시에 저장된 데이터 반환. 만료 여부 무관. 없으면 None."""
        entry = self._store.get(self._key(city, station_id))
        return entry["data"] if entry else None


# 전역 싱글턴 — 서버 프로세스 내 공유
arrival_cache = ArrivalCache(ttl_seconds=30)
