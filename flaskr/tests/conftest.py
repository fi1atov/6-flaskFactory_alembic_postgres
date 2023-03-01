import pytest

from module_29_testing.hw.flaskr import create_app, db as _db
from module_29_testing.hw.flaskr.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app('autotesting')

    with _app.app_context():
        _db.create_all()
        client = Client(name="Василий", surname="Иванов", credit_card="2356", car_number="15354862")
        parking = Parking(address="Волгоград", opened=True, count_places=50, count_available_places=50)
        client_parking = ClientParking(client_id=1, parking_id=1, time_in="2023-01-31 00:37:06.515299")

        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
