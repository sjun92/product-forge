from models import User
from auth.jwt_utils import create_access_token


def _admin_cookie(client, db):
    admin = User(email="admin@example.com", name="관리자",
                 is_approved=True, is_admin=True)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    token = create_access_token(admin.id)
    client.cookies.set("access_token", token)
    return admin


def _regular_cookie(client, db):
    user = User(email="user@example.com", name="일반",
                is_approved=True, is_admin=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    client.cookies.set("access_token", token)
    return user


def test_admin_lists_users(client, db):
    _admin_cookie(client, db)
    pending = User(email="p@example.com", name="대기", is_approved=False)
    db.add(pending)
    db.commit()

    resp = client.get("/admin/users")
    assert resp.status_code == 200
    emails = [u["email"] for u in resp.json()]
    assert "p@example.com" in emails


def test_non_admin_blocked(client, db):
    _regular_cookie(client, db)
    resp = client.get("/admin/users")
    assert resp.status_code == 403


def test_admin_approves_user(client, db):
    _admin_cookie(client, db)
    pending = User(email="p@example.com", name="대기", is_approved=False)
    db.add(pending)
    db.commit()
    db.refresh(pending)

    resp = client.patch(f"/admin/users/{pending.id}/approve",
                        json={"is_approved": True})
    assert resp.status_code == 200

    db.refresh(pending)
    assert pending.is_approved is True
