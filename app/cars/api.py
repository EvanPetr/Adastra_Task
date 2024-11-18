from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.cars.filters import CarFilter
from app.cars.models import Car
from app.cars.repository import CarRepository, get_repository
from app.cars.schemas.request import CarRequest
from app.cars.schemas.response import CarResponse as CarsResponse
from app.database import get_db
from app.utils import check_user_authorization

router_car: APIRouter = APIRouter(prefix="/cars", tags=["Cars"])

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


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


@router_car.get(
    "/{car_id:uuid}", status_code=status.HTTP_200_OK, response_model=CarsResponse
)
def get_car(
    car_id: UUID,
    repository: CarRepository = Depends(get_repository(CarRepository)),
) -> CarsResponse:
    return repository.get_one(car_id=car_id)


@router_car.post("", status_code=status.HTTP_201_CREATED, response_model=CarsResponse)
def create_car(
    car_request: CarRequest,
    repository: CarRepository = Depends(get_repository(CarRepository)),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> CarsResponse:
    check_user_authorization(token=token, db=db)

    car: Car = repository.create(car_request=car_request)

    return car


@router_car.put(
    "/{car_id:uuid}", status_code=status.HTTP_200_OK, response_model=CarsResponse
)
def update_car(
    car_id: UUID,
    car_request: CarRequest,
    repository: CarRepository = Depends(get_repository(CarRepository)),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> CarsResponse:
    check_user_authorization(token=token, db=db)

    persisted_car: Car = repository.update(car_id=car_id, car_request=car_request)

    return persisted_car


@router_car.delete(
    "/{car_id:uuid}", status_code=status.HTTP_204_NO_CONTENT, response_model={}
)
def delete_car(
    car_id: UUID,
    repository: CarRepository = Depends(get_repository(CarRepository)),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> dict:
    check_user_authorization(token=token, db=db)

    repository.delete(car_id=car_id)

    return {}
