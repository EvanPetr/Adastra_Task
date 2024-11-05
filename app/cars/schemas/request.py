from pydantic import BaseModel


class CarRequest(BaseModel):
    brand: str
    model: str
