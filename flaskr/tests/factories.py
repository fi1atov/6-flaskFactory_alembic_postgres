import factory
import factory.fuzzy as fuzzy
import random

from module_29_testing.hw.flaskr import db as _db
from module_29_testing.hw.flaskr.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = _db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = "1245"
    car_number = fuzzy.FuzzyText(length=8, chars=[str(num) for num in range(10)])


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = _db.session

    address = factory.Faker('address')
    opened = bool(random.choice([True, False]))
    count_places = random.choice([0, 5, 10])
    count_available_places = factory.LazyAttribute(lambda x: random.randrange(50, 100))
