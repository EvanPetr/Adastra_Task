from collections.abc import Generator
from datetime import datetime, UTC

from app.password import pwd_context

import pytest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.config import DATABASE_URL
from app.cars.models.car import Car
from uuid import UUID
from app.users.models.user import User

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session]:
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(db_session) -> Generator[TestClient]:
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def car_id() -> UUID:
    """Generate a random user id."""
    return uuid.uuid4()


@pytest.fixture
def car_request_body() -> dict:
    return {
        "brand": "TestBrand",
        "model": "TestModel",
    }


@pytest.fixture
def car_response_body(car_id: UUID) -> dict:
    return {
        "id": str(car_id),
        "brand": "TestBrand",
        "model": "TestModel",
    }


@pytest.fixture
def cars_empty_response() -> dict:
    return {
        "items": [],
        "page": 1,
        "pages": 0,
        "size": 50,
        "total": 0,
    }


@pytest.fixture
def cars_response(car_id: UUID) -> dict:
    return {
        "items": [
            {
                "id": str(car_id),
                "brand": "BrandTest",
                "model": "ModelTest",
                "created_at": "2024-11-05T00:00:00Z",
                "updated_at": "2024-11-05T00:00:00Z",
            }
        ],
        "page": 1,
        "pages": 1,
        "size": 50,
        "total": 1,
    }


@pytest.fixture
def datetime_stamp() -> datetime:
    return datetime(year=2024, month=11, day=5, tzinfo=UTC)


@pytest.fixture
def car_model(car_id: UUID, datetime_stamp: datetime) -> Car:
    return Car(
        id=car_id,
        brand="BrandTest",
        model="ModelTest",
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )


@pytest.fixture
def bearer_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4Y2Q1NmU5Yy02ODY5LTQ3NGYtOGVlOC1iYTQzZWZkZmEyNjAiLCJleHAiOjE3MzA4MDk4MDB9.SPFrAT3wrtv2c5Bbu3WT6t4j5uauAWdin7HqEngFC6U"


@pytest.fixture
def auth_invalid_bearer_header() -> dict:
    return {"Authorization": "Bearer test"}


@pytest.fixture
def auth_bearer_header(bearer_token: str) -> dict:
    return {"Authorization": f"Bearer {bearer_token}"}


@pytest.fixture
def user_id() -> UUID:
    """Generate a random user id."""
    return UUID("8cd56e9c-6869-474f-8ee8-ba43efdfa260")


@pytest.fixture
def user_model(user_id: UUID, datetime_stamp: datetime) -> User:
    return User(
        id=user_id,
        name="TestName",
        email="test@test.com",
        password=pwd_context.hash("test"),
        created_at=datetime_stamp,
        updated_at=datetime_stamp,
    )


@pytest.fixture
def user_login_request() -> dict:
    return {"email": "test@test.com", "password": "test"}


@pytest.fixture
def user_register_request() -> dict:
    return {"name": "TesName", "email": "test@test.com", "password": "test"}


@pytest.fixture
def user_wrong_creds_login_request() -> dict:
    return {"email": "test@test.com", "password": "testtest"}


@pytest.fixture
def user_profile_response() -> dict:
    return {"email": "test@test.com", "name": "TestName"}
