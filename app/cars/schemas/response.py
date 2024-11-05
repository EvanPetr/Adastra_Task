from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class CarResponse(BaseModel):
    id: UUID
    brand: str
    model: str
    created_at: datetime
    updated_at: datetime
