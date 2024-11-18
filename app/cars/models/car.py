import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.cars.schemas.request import CarRequest
from app.database import Base


class Car(Base):
    __tablename__ = "car"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    brand: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("Now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), onupdate=text("Now()"), server_default=text("Now()")
    )

    def merge(self, other: CarRequest) -> "Car":
        self.brand = other.brand
        self.model = other.model

        return self
