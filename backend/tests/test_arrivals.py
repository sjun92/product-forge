import time
from arrivals.cache import ArrivalCache


def test_cache_miss_calls_fetcher():
    calls = []

    def fetcher(station_id):
        calls.append(station_id)
        return [{"route_name": "147", "arrival_msg": "3분"}]

    cache = ArrivalCache(ttl_seconds=30)
    result = cache.get("seoul", "S1", fetcher)
    assert result == [{"route_name": "147", "arrival_msg": "3분"}]
    assert len(calls) == 1


def test_cache_hit_skips_fetcher():
    calls = []

    def fetcher(station_id):
        calls.append(station_id)
        return [{"route_name": "147", "arrival_msg": "3분"}]

    cache = ArrivalCache(ttl_seconds=30)
    cache.get("seoul", "S1", fetcher)
    cache.get("seoul", "S1", fetcher)
    assert len(calls) == 1   # 두 번 호출해도 fetcher는 1번만


def test_cache_expired_calls_fetcher_again():
    calls = []

    def fetcher(station_id):
        calls.append(station_id)
        return []

    cache = ArrivalCache(ttl_seconds=0)   # 즉시 만료
    cache.get("seoul", "S1", fetcher)
    time.sleep(0.01)
    cache.get("seoul", "S1", fetcher)
    assert len(calls) == 2
