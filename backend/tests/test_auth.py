from auth.jwt_utils import create_access_token, decode_access_token

def test_jwt_roundtrip():
    token = create_access_token(user_id=42)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"

def test_jwt_invalid_raises():
    import pytest
    with pytest.raises(Exception):
        decode_access_token("not.a.valid.token")


from fastapi import Request
from unittest.mock import MagicMock
from auth.dependencies import get_current_user, require_approved, require_admin
from models import User


def _make_request(token):
    req = MagicMock(spec=Request)
    req.cookies = {"access_token": token} if token else {}
    return req


def test_get_current_user_no_cookie(db):
    from fastapi import HTTPException
    import pytest
    req = _make_request(None)
    with pytest.raises(HTTPException) as exc:
        get_current_user(req, db)
    assert exc.value.status_code == 401


def test_get_current_user_invalid_token(db):
    from fastapi import HTTPException
    import pytest
    req = _make_request("bad.token.here")
    with pytest.raises(HTTPException) as exc:
        get_current_user(req, db)
    assert exc.value.status_code == 401


def test_require_approved_blocks_pending(db):
    from fastapi import HTTPException
    import pytest
    user = User(email="pending@example.com", name="대기", is_approved=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    with pytest.raises(HTTPException) as exc:
        require_approved(user)
    assert exc.value.status_code == 403


def test_require_admin_blocks_non_admin(db):
    from fastapi import HTTPException
    import pytest
    user = User(email="user@example.com", name="일반", is_approved=True, is_admin=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    with pytest.raises(HTTPException) as exc:
        require_admin(user)
    assert exc.value.status_code == 403
