import pytest
from models import User, Favorite
from auth.jwt_utils import create_access_token


def _auth_cookie(client, db):
    user = User(email="u@example.com", name="유저", is_approved=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    client.cookies.set("access_token", token)
    return user


def test_add_and_list_favorites(client, db):
    user = _auth_cookie(client, db)
    resp = client.post("/favorites", json={
        "station_id": "111000001",
        "station_name": "강남역",
        "city": "seoul",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["station_name"] == "강남역"

    resp2 = client.get("/favorites")
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1


def test_delete_favorite(client, db):
    user = _auth_cookie(client, db)
    fav = Favorite(user_id=user.id, station_id="X", station_name="X역",
                   city="seoul", display_order=0)
    db.add(fav)
    db.commit()
    db.refresh(fav)

    resp = client.delete(f"/favorites/{fav.id}")
    assert resp.status_code == 200

    resp2 = client.get("/favorites")
    assert resp2.json() == []


def test_reorder_favorites(client, db):
    user = _auth_cookie(client, db)
    fav1 = Favorite(user_id=user.id, station_id="A", station_name="A역",
                    city="seoul", display_order=0)
    fav2 = Favorite(user_id=user.id, station_id="B", station_name="B역",
                    city="seoul", display_order=1)
    db.add_all([fav1, fav2])
    db.commit()
    db.refresh(fav1)
    db.refresh(fav2)

    resp = client.patch("/favorites/reorder",
                        json={"order": [fav2.id, fav1.id]})
    assert resp.status_code == 200

    resp2 = client.get("/favorites")
    items = resp2.json()
    assert items[0]["id"] == fav2.id
    assert items[1]["id"] == fav1.id


def test_delete_others_favorite_denied(client, db):
    user = _auth_cookie(client, db)
    other = User(email="other@example.com", name="타인", is_approved=True)
    db.add(other)
    db.commit()
    db.refresh(other)
    fav = Favorite(user_id=other.id, station_id="Z", station_name="Z역",
                   city="seoul", display_order=0)
    db.add(fav)
    db.commit()
    db.refresh(fav)

    resp = client.delete(f"/favorites/{fav.id}")
    assert resp.status_code == 403
