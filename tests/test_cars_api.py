from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
from app.cars.models.car import Car
from uuid import UUID
from app.users.models.user import User
from freezegun import freeze_time


def test_get_cars_empty(test_client: TestClient, cars_empty_response: dict):
    response = test_client.get("/cars")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == cars_empty_response


def test_get_cars(
    db_session: Session, test_client: TestClient, car_model, cars_response: dict
):
    db_session.add(car_model)
    db_session.commit()

    response = test_client.get("/cars")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == cars_response


def test_get_cars_search(
    db_session: Session, test_client: TestClient, car_model: Car, cars_response: dict
):
    db_session.add(car_model)
    db_session.commit()

    response = test_client.get("/cars", params={"search": "Test"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == cars_response


def test_get_cars_search_empty_response(
    db_session: Session,
    test_client: TestClient,
    car_model: Car,
    cars_empty_response: dict,
):
    db_session.add(car_model)
    db_session.commit()

    response = test_client.get("/cars", params={"search": "Opel"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == cars_empty_response


@freeze_time("2024-11-05T12:00:00+00:00")
def test_create_car(
    db_session: Session,
    test_client: TestClient,
    car_request_body: dict,
    car_response_body: dict,
    user_model: User,
    auth_bearer_header: dict,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.post(
        "/cars", json=car_request_body, headers=auth_bearer_header
    )

    created_car: dict = response.json()
    car_response_body |= {"id": created_car["id"]}

    assert response.status_code == status.HTTP_201_CREATED
    assert car_response_body.items() <= created_car.items()


@freeze_time("2024-11-05T12:00:00+00:00")
def test_update_car_not_found(
    db_session: Session,
    test_client: TestClient,
    user_model: User,
    auth_bearer_header: dict,
    car_request_body: dict,
    car_response_body: dict,
    car_id: UUID,
):
    db_session.add(user_model)
    db_session.commit()

    response = test_client.put(
        f"/cars/{car_id}", json=car_request_body, headers=auth_bearer_header
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Car with id <{car_id}> does not exists!"}


@freeze_time("2024-11-05T12:00:00+00:00")
def test_update_car(
    db_session: Session,
    test_client: TestClient,
    user_model: User,
    auth_bearer_header: dict,
    car_request_body: dict,
    car_response_body: dict,
    car_id: UUID,
    car_model: Car,
):
    db_session.add_all([user_model, car_model])
    db_session.commit()

    response = test_client.put(
        f"/cars/{car_id}", json=car_request_body, headers=auth_bearer_header
    )

    assert response.status_code == status.HTTP_200_OK
    assert car_response_body.items() <= response.json().items()


@freeze_time("2024-11-05T12:00:00+00:00")
def test_delete_car(
    db_session: Session,
    test_client: TestClient,
    user_model: User,
    auth_bearer_header: dict,
    car_request_body: dict,
    car_response_body: dict,
    car_id: UUID,
    car_model: Car,
):
    db_session.add_all([user_model, car_model])
    db_session.commit()

    response = test_client.delete(f"/cars/{car_id}", headers=auth_bearer_header)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert db_session.query(Car).where(Car.id == car_id).first() is None
