import time
from unittest.mock import patch
from arrivals.cache import ArrivalCache
from models import User
from auth.jwt_utils import create_access_token


# ── 캐시 단위 테스트 ──────────────────────────────────────

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
    assert len(calls) == 1


def test_cache_expired_calls_fetcher_again():
    calls = []

    def fetcher(station_id):
        calls.append(station_id)
        return []

    cache = ArrivalCache(ttl_seconds=0)
    cache.get("seoul", "S1", fetcher)
    time.sleep(0.01)
    cache.get("seoul", "S1", fetcher)
    assert len(calls) == 2


# ── 라우터 통합 테스트 ────────────────────────────────────

def _auth_cookie(client, db):
    user = User(email="u@example.com", name="유저", is_approved=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    client.cookies.set("access_token", token)
    return user


MOCK_ARRIVALS = [{"route_name": "147", "arrival_msg": "3분", "arrival_msg2": "8분"}]


def test_arrivals_seoul_returns_data(client, db):
    _auth_cookie(client, db)
    with patch("arrivals.router.arrival_cache") as mock_cache:
        mock_cache.get.return_value = MOCK_ARRIVALS
        resp = client.get("/arrivals?station_id=S1&city=seoul")
    assert resp.status_code == 200
    data = resp.json()
    assert data["stale"] is False
    assert data["arrivals"] == MOCK_ARRIVALS


def test_arrivals_gyeonggi_returns_data(client, db):
    _auth_cookie(client, db)
    with patch("arrivals.router.arrival_cache") as mock_cache:
        mock_cache.get.return_value = MOCK_ARRIVALS
        resp = client.get("/arrivals?station_id=G1&city=gyeonggi")
    assert resp.status_code == 200
    assert resp.json()["stale"] is False


def test_arrivals_api_failure_returns_stale(client, db):
    _auth_cookie(client, db)
    with patch("arrivals.router.arrival_cache") as mock_cache:
        mock_cache.get.side_effect = Exception("API 타임아웃")
        mock_cache.get_stale.return_value = MOCK_ARRIVALS
        resp = client.get("/arrivals?station_id=S1&city=seoul")
    assert resp.status_code == 200
    data = resp.json()
    assert data["stale"] is True
    assert data["arrivals"] == MOCK_ARRIVALS


def test_arrivals_api_failure_no_stale_returns_empty(client, db):
    _auth_cookie(client, db)
    with patch("arrivals.router.arrival_cache") as mock_cache:
        mock_cache.get.side_effect = Exception("API 오류")
        mock_cache.get_stale.return_value = None
        resp = client.get("/arrivals?station_id=S1&city=seoul")
    assert resp.status_code == 200
    data = resp.json()
    assert data["stale"] is True
    assert data["arrivals"] == []


def test_arrivals_unapproved_user_blocked(client, db):
    user = User(email="pending@example.com", name="대기", is_approved=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    client.cookies.set("access_token", token)
    resp = client.get("/arrivals?station_id=S1&city=seoul")
    assert resp.status_code == 403


def test_arrivals_invalid_city_rejected(client, db):
    _auth_cookie(client, db)
    resp = client.get("/arrivals?station_id=S1&city=busan")
    assert resp.status_code == 422
