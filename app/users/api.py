from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.users.schemas.response import Profile
from app.utils import check_user_authorization

router_user: APIRouter = APIRouter(prefix="/user", tags=["User"])

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


@router_user.get("/profile", status_code=status.HTTP_200_OK, response_model=Profile)
def get_user_profile(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Profile:
    persisted_user = check_user_authorization(token=token, db=db)

    return persisted_user
