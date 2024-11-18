from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.cars.models.car import Car
from app.cars.schemas.request import CarRequest
from app.database import get_db


class CarRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get_instance(self, car_id: UUID) -> Car | None:
        return self.session.query(Car).filter(Car.id == car_id).first()

    def get_one(self, car_id: UUID) -> Car:
        persisted_car: Car | None = self._get_instance(car_id=car_id)

        if not persisted_car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Car with id <{car_id}> does not exists!",
            )

        return persisted_car

    def create(self, car_request: CarRequest) -> Car:
        car: Car = Car(brand=car_request.brand, model=car_request.model)

        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)

        return car

    def update(self, car_id: UUID, car_request: CarRequest) -> Car:
        persisted_car: Car | None = self._get_instance(car_id=car_id)

        if not persisted_car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Car with id <{car_id}> does not exists!",
            )

        persisted_car.merge(car_request)
        self.session.commit()

        return persisted_car

    def delete(self, car_id: UUID) -> None:
        persisted_car: Car | None = self._get_instance(car_id=car_id)

        if persisted_car:
            self.session.delete(persisted_car)
            self.session.commit()


def get_repository(repository):
    def _get_repository(session: Session = Depends(get_db)):
        return repository(session)

    return _get_repository
