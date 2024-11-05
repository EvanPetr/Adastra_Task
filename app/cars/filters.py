from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from app.cars.models.car import Car


class CarFilter(Filter):
    brand: Optional[str] = None
    model: Optional[str] = None

    class Constants(Filter.Constants):
        model = Car
