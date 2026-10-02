from models import User, Favorite
from sqlalchemy.orm import Session


def test_create_user(db: Session):
    user = User(email="test@example.com", name="테스터")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.is_approved is False
    assert user.is_admin is False


def test_create_favorite(db: Session):
    user = User(email="test@example.com", name="테스터", is_approved=True)
    db.add(user)
    db.commit()

    fav = Favorite(
        user_id=user.id,
        station_id="111000001",
        station_name="강남역",
        city="seoul",
        display_order=0,
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)

    assert fav.id is not None
    assert fav.user_id == user.id
