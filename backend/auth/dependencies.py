from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from auth.jwt_utils import decode_access_token
from database import get_db
from models import User


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="유효하지 않은 인증 정보입니다")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")
    return user


def require_approved(user: User = Depends(get_current_user)) -> User:
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="관리자 승인 후 이용 가능합니다")
    return user


def require_admin(user: User = Depends(require_approved)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다")
    return user
