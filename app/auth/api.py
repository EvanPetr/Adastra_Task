from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.schemas.request import LoginInput, RegisterInput
from app.database import get_db
from app.password import hash_password, verify_password
from app.token import create_access_token
from app.users.models.user import User

router_auth: APIRouter = APIRouter(prefix="/auth", tags=["Auth"])


# Login endpoint
@router_auth.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
def login(body: LoginInput, db: Session = Depends(get_db)) -> dict:
    persisted_user: User | None = (
        db.query(User).filter(User.email == body.email).first()
    )

    if not persisted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    verify = verify_password(body.password, persisted_user.password)

    if not verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(persisted_user.id)})

    return {"access_token": access_token}


# Register endpoint
@router_auth.post("/register", status_code=status.HTTP_200_OK, response_model=dict)
def register(body: RegisterInput, db: Session = Depends(get_db)) -> dict:
    persisted_user: User | None = (
        db.query(User).filter(User.email == body.email).first()
    )

    if persisted_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hashed_password = hash_password(body.password)
    user = User(name=body.name, email=body.email, password=hashed_password)
    db.add(user)
    db.commit()

    return {"message": "User created successfully"}
