from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CarResponse(BaseModel):
    id: UUID
    brand: str
    model: str
    created_at: datetime
    updated_at: datetime
