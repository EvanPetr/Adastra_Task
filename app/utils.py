from fastapi import HTTPException, status
from app.users.models.user import User
from sqlalchemy.orm import Session
from app.token import decode_token
from uuid import UUID


def check_user_authorization(token: str, db: Session) -> User:
    user_id: UUID = decode_token(token)
    persisted_user: User | None = db.query(User).filter(User.id == user_id).first()

    if not persisted_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return persisted_user
