from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
from app.users.models.user import User
from freezegun import freeze_time


def test_user_login_does_not_exists(
    test_client: TestClient,
    auth_bearer_header: dict,
    user_login_request: dict,
):
    response = test_client.post("/auth/login", json=user_login_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Incorrect email or password",
    }


def test_user_login_exists_wrong_creds(
    db_session: Session,
    test_client: TestClient,
    user_wrong_creds_login_request: dict,
    user_model: User,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.post("/auth/login", json=user_wrong_creds_login_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Incorrect email or password",
    }


@freeze_time("2024-11-05T12:00:00+00:00")
def test_user_login_exists_correct_creds(
    db_session: Session,
    test_client: TestClient,
    user_login_request: dict,
    user_model: User,
    bearer_token: str,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.post("/auth/login", json=user_login_request)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": bearer_token,
    }


def test_user_register(
    test_client: TestClient,
    user_register_request: dict,
):
    response = test_client.post("/auth/register", json=user_register_request)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "User created successfully",
    }


def test_user_register_exists_error(
    db_session: Session,
    test_client: TestClient,
    user_model: User,
    user_register_request: dict,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.post("/auth/register", json=user_register_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Email already exists",
    }
