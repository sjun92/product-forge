from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.dependencies import require_approved
from database import get_db
from models import Favorite, User

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteCreate(BaseModel):
    station_id: str
    station_name: str
    city: str   # 'seoul' | 'gyeonggi'


class ReorderRequest(BaseModel):
    order: list[int]  # favorite id 순서 배열


@router.get("")
def list_favorites(
    user: User = Depends(require_approved),
    db: Session = Depends(get_db),
):
    favs = (
        db.query(Favorite)
        .filter(Favorite.user_id == user.id)
        .order_by(Favorite.display_order)
        .all()
    )
    return [
        {
            "id": f.id,
            "station_id": f.station_id,
            "station_name": f.station_name,
            "city": f.city,
            "display_order": f.display_order,
        }
        for f in favs
    ]


@router.post("")
def add_favorite(
    body: FavoriteCreate,
    user: User = Depends(require_approved),
    db: Session = Depends(get_db),
):
    count = db.query(Favorite).filter(Favorite.user_id == user.id).count()
    fav = Favorite(
        user_id=user.id,
        station_id=body.station_id,
        station_name=body.station_name,
        city=body.city,
        display_order=count,
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return {"id": fav.id, "station_id": fav.station_id,
            "station_name": fav.station_name, "city": fav.city,
            "display_order": fav.display_order}


@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    user: User = Depends(require_approved),
    db: Session = Depends(get_db),
):
    fav = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="즐겨찾기를 찾을 수 없습니다")
    if fav.user_id != user.id:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다")
    db.delete(fav)
    db.commit()
    return {"message": "삭제 완료"}


@router.patch("/reorder")
def reorder_favorites(
    body: ReorderRequest,
    user: User = Depends(require_approved),
    db: Session = Depends(get_db),
):
    for order, fav_id in enumerate(body.order):
        db.query(Favorite).filter(
            Favorite.id == fav_id,
            Favorite.user_id == user.id,
        ).update({"display_order": order})
    db.commit()
    return {"message": "순서 변경 완료"}
