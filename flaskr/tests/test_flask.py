import json
import pytest


# def test_math_route(client) -> None:
#     resp = client.get("/test_route?number=8")
#     data = json.loads(resp.data.decode())
#     assert data == 64

@pytest.fixture()
def add_client(client):
    client_data = {"name": "Александр", "surname": "Пушкин",
                   "credit_card": "6682", "car_number": "56235622"}
    resp = client.post("/clients", json=client_data)
    return resp

@pytest.fixture()
def add_parking(client):
    parking_data = {"address": "Тюмень", "opened": 1,
                    "count_places": 0, "count_available_places": 60}
    resp = client.post("/parkings", json=parking_data)
    return resp


def test_get_client_by_id(client) -> None:
    resp = client.get("/clients/1")
    assert resp.status_code == 200
    assert resp.json == {"id": 1, "name": "Василий", "surname": "Иванов",
                         "credit_card": "2356", "car_number": "15354862"}

def test_get_clients(client) -> None:
    resp = client.get("/clients")
    result = resp.json['client_list']
    assert isinstance(result, list)
    assert resp.status_code == 200


@pytest.mark.parametrize("route", ["/clients/1", "/clients"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(add_client) -> None:
    resp = add_client
    assert resp.status_code == 201


def test_create_parking(add_parking) -> None:
    resp = add_parking
    assert resp.status_code == 201

@pytest.mark.parking
def test_come_to_parking(client, add_client, add_parking) -> None:
    resp = add_client
    assert resp.status_code == 201
    resp = add_parking
    assert resp.status_code == 201
    client_parking_data = {"client_id": 2, "parking_id": 2}
    resp = client.post("/client_parkings", json=client_parking_data)
    assert resp.status_code == 201

@pytest.mark.parking
def test_leave_parking(client) -> None:
    parking_data = {"client_id": 1, "parking_id": 1}
    resp = client.delete("/client_parkings", json=parking_data)
    assert resp.status_code == 201


def test_app_config(app):
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "postgresql+psycopg2://postgres:postgres@localhost:5432/skillbox_test"



# @pytest.mark.parametrize("route", ["/test_route?number=8", "/users/1",
#                                    "/users", "/"])
# def test_route_status(client, route):
#     rv = client.get(route)
#     assert rv.status_code == 200
