from unittest.mock import patch
from models import User
from auth.jwt_utils import create_access_token


def _auth_cookie(client, db):
    user = User(email="u@example.com", name="유저", is_approved=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    client.cookies.set("access_token", token)
    return user


def test_search_stations_returns_merged_results(client, db):
    _auth_cookie(client, db)
    mock_seoul = [{"station_id": "S1", "station_name": "강남역", "city": "seoul"}]
    mock_gyeonggi = [{"station_id": "G1", "station_name": "강남버스터미널", "city": "gyeonggi"}]

    with patch("search.router.search_stations_seoul", return_value=mock_seoul), \
         patch("search.router.search_stations_gyeonggi", return_value=mock_gyeonggi):
        resp = client.get("/search/stations?q=강남")

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 2


def test_search_stations_partial_failure(client, db):
    _auth_cookie(client, db)
    mock_seoul = [{"station_id": "S1", "station_name": "강남역", "city": "seoul"}]

    with patch("search.router.search_stations_seoul", return_value=mock_seoul), \
         patch("search.router.search_stations_gyeonggi", side_effect=Exception("timeout")):
        resp = client.get("/search/stations?q=강남")

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 1
    assert len(data["errors"]) == 1
