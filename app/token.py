from datetime import UTC, datetime, timedelta
from typing import Final
from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt

SECRET_KEY: Final[str] = "tWFG0dbklgahLxKyj5BbFy44td8wRZns"
ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 30


def create_access_token(data: dict) -> str:
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(tz=UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> UUID:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: UUID = UUID(payload.get("sub"))
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
