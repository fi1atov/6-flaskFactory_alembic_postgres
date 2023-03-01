from datetime import datetime

from . import db
from typing import Dict, Any


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.Sequence('client_id_seq'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return f"Client {self.name} {self.surname}"

    @classmethod
    def get_client_card(cls, client_id: int):
        try:
            client_card = db.session.query(Client.credit_card).filter(cls.id == client_id).one()
            return client_card[0]
        except Exception:
            raise Exception("No client with id {} was found".format(client_id))

    @classmethod
    def get_client_by_id(cls, client_id: int):
        try:
            # client = db.session.query(Client).filter(cls.id == client_id).one()
            client = db.session.query(Client).get(client_id)
            return client
        except Exception:
            raise Exception("No client with id {} was found".format(client_id))

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parking'

    id = db.Column(db.Integer, db.Sequence('parking_id_seq'), primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    @classmethod
    def is_available_places(cls, parking_id: int):
        try:
            available_places = db.session.query(Parking.count_available_places).filter(cls.id == parking_id).one()
            if available_places[0] > 0:
                return True
            else:
                return False

        except Exception:
            raise Exception("No client with id {} was found".format(parking_id))

    @classmethod
    def update_parking_places(cls, parking_id: int, is_upper: bool = False):
        """
            is_upper = True     - Клиент уехал
            is_upper = False    - Клиент приехал
        """
        try:
            parking = cls.get_parking_by_id(parking_id)
            if is_upper:
                parking.count_available_places += 1
                parking.count_places -= 1
            else:
                parking.count_available_places -= 1
                parking.count_places += 1

            return parking

        except Exception:
            raise Exception("Error while updating parking places")

    @classmethod
    def is_open(cls, parking_id: int):
        try:
            is_open_parking = db.session.query(Parking.opened).filter(cls.id == parking_id).one()
            return is_open_parking[0]   # костыль, т.к. тут возвращается dict
        except Exception:
            raise Exception("No client with id {} was found".format(parking_id))

    @classmethod
    def get_parking_by_id(cls, parking_id: int):
        try:
            parking = db.session.query(Parking).get(parking_id)
            return parking
        except Exception:
            raise Exception("No client with id {} was found".format(parking_id))

    def __repr__(self):
        return f"Parking {self.address}"


class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, db.Sequence('client_parking_id_seq'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship("Client", backref="client_parking")
    parking = db.relationship("Parking", backref="client_parking")
    __table_args__ = (db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),)

    def __repr__(self):
        return f"ClientParking"

    # @classmethod
    # def update_time_out(cls, client_id: int, parking_id: int):
    #     try:
    #         client_parking = cls.get_client_parking_by_id(client_id, parking_id)
    #         client_parking.time_out = datetime.now()
    #
    #         return client_parking
    #
    #     except Exception:
    #         raise Exception("Error while updating client_parking time_out")

    @classmethod
    def get_client_parking_by_id(cls, client_id: int, parking_id: int):
        try:
            client_parking = db.session.query(ClientParking).filter(
                cls.client_id == client_id,
                cls.parking_id == parking_id
            ).one()
            return client_parking
        except Exception:
            raise Exception("No client_parking with id's {}/{} was found".format(client_id, parking_id))


class ClientParkingLog(db.Model):
    __tablename__ = 'client_parking_log'

    id = db.Column(db.Integer, db.Sequence('client_parking_log_id_seq'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)

    client = db.relationship("Client", backref="client_parking_log")
    parking = db.relationship("Parking", backref="client_parking_log")

    def __repr__(self):
        return f"Parking on {self.address}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

    @classmethod
    def update_time_out(cls, client_id: int, parking_id: int):
        try:
            client_parking_log = cls.get_client_parking_log_by_id(client_id, parking_id)
            client_parking_log.time_out = datetime.now()

            return client_parking_log

        except Exception:
            raise Exception("Error while updating client_parking time_out")

    @classmethod
    def get_client_parking_log_by_id(cls, client_id: int, parking_id: int):
        try:
            client_parking_log = db.session.query(ClientParkingLog).filter(
                cls.client_id == client_id,
                cls.parking_id == parking_id,
                cls.time_out is None
            ).one()
            return client_parking_log
        except Exception:
            raise Exception("No client_parking with id's {}/{} was found".format(client_id, parking_id))