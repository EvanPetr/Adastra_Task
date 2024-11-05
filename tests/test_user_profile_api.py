from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
from uuid import UUID
from app.users.models.user import User
from freezegun import freeze_time


@freeze_time("2024-11-05T12:00:00+00:00")
def test_get_user_profile_does_not_exists_raises_unauthorized(
    test_client: TestClient,
    user_id: UUID,
    auth_bearer_header: dict,
):
    response = test_client.get("/user/profile", headers=auth_bearer_header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid authentication credentials"}


def test_get_user_profile_invalid_bearer_token_raises_unauthorized(
    test_client: TestClient,
    user_id: UUID,
    auth_invalid_bearer_header: dict,
):
    response = test_client.get("/user/profile", headers=auth_invalid_bearer_header)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Unauthorized"}


@freeze_time("2024-11-05T12:00:00+00:00")
def test_get_user_profile_authorized(
    db_session: Session,
    test_client: TestClient,
    user_id: UUID,
    user_model: User,
    user_profile_response: dict,
    auth_bearer_header: dict,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.get("/user/profile", headers=auth_bearer_header)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_profile_response
