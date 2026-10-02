from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import httpx

from config import settings
from database import get_db
from models import User
from auth.jwt_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.get("/google")
def google_login():
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/callback")
def google_callback(code: str, response: Response, db: Session = Depends(get_db)):
    # 1. 코드 → access_token 교환
    token_data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }
    token_resp = httpx.post(GOOGLE_TOKEN_URL, data=token_data)
    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Google 토큰 교환 실패")
    access_token = token_resp.json()["access_token"]

    # 2. 사용자 정보 조회
    user_resp = httpx.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if user_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Google 사용자 정보 조회 실패")
    google_user = user_resp.json()
    email = google_user["email"]
    name = google_user.get("name", email)

    # 3. DB upsert
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 4. 첫 번째 관리자 부트스트랩
    if email == settings.first_admin_email and not user.is_admin:
        user.is_admin = True
        user.is_approved = True
        db.commit()

    # 5. JWT → httpOnly cookie
    jwt_token = create_access_token(user.id)
    redirect = RedirectResponse(url=f"{settings.frontend_url}/")
    redirect.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,
        max_age=settings.jwt_expire_hours * 3600,
        samesite="lax",
    )
    return redirect


@router.get("/me")
def get_me(request: Request, db: Session = Depends(get_db)):
    from auth.dependencies import get_current_user
    user = get_current_user(request, db)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "is_approved": user.is_approved,
        "is_admin": user.is_admin,
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "로그아웃 완료"}
