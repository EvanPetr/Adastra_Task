from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.database import get_db
from sqlalchemy.orm import Session
from app.cars.models import Car
from app.cars.schemas.request import CarRequest
from app.cars.schemas.response import CarResponse as CarsResponse
from uuid import UUID
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from app.cars.filters import CarFilter
from fastapi_filter import FilterDepends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_
from app.utils import check_user_authorization

router_car: APIRouter = APIRouter(prefix="/cars", tags=["Cars"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router_car.get("", status_code=status.HTTP_200_OK, response_model=Page[CarsResponse])
def get_cars(
    search: str | None = None,
    car_filter: CarFilter = FilterDepends(CarFilter),
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Page[CarsResponse]:
    filters: list = []
    if search:
        filters.append(or_(Car.brand.contains(search), Car.model.contains(search)))
    query = car_filter.filter(select(Car).where(*filters).offset(offset).limit(limit))

    return paginate(db, query)


@router_car.post("", status_code=status.HTTP_201_CREATED, response_model=CarsResponse)
def create_car(
    car_request: CarRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> CarsResponse:
    check_user_authorization(token=token, db=db)

    car: Car = Car(brand=car_request.brand, model=car_request.model)

    db.add(car)
    db.commit()
    db.refresh(car)

    return car


@router_car.put(
    "/{car_id:uuid}", status_code=status.HTTP_200_OK, response_model=CarsResponse
)
def update_car(
    car_id: UUID,
    car: CarRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> CarsResponse:
    check_user_authorization(token=token, db=db)

    persisted_car: Car | None = db.query(Car).filter(Car.id == car_id).first()

    if not persisted_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id <{car_id}> does not exists!",
        )

    persisted_car.merge(car)
    db.commit()

    return persisted_car


@router_car.delete(
    "/{car_id:uuid}", status_code=status.HTTP_204_NO_CONTENT, response_model={}
)
def delete_car(
    car_id: UUID, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> dict:
    check_user_authorization(token=token, db=db)

    persisted_car: Car | None = db.query(Car).filter(Car.id == car_id).first()

    if persisted_car:
        db.delete(persisted_car)
        db.commit()

    return {}
