from auth.jwt_utils import create_access_token, decode_access_token

def test_jwt_roundtrip():
    token = create_access_token(user_id=42)
    payload = decode_access_token(token)
    assert payload["sub"] == "42"

def test_jwt_invalid_raises():
    import pytest
    with pytest.raises(Exception):
        decode_access_token("not.a.valid.token")
