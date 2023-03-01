from datetime import datetime
from flask import Blueprint, jsonify, request

from module_29_testing.hw.flaskr.models import Client
from module_29_testing.hw.flaskr.models import Parking
from module_29_testing.hw.flaskr.models import ClientParking
from module_29_testing.hw.flaskr.models import ClientParkingLog

from module_29_testing.hw.flaskr import db
from module_29_testing.hw.flaskr.log import log

bp = Blueprint('client_parkings', __name__)


@bp.route('/client_parkings', methods=['POST'])
def add_client_parking():

    try:
        data = request.get_json()

        client_id = data["client_id"]
        parking_id = data["parking_id"]

        client: Client = Client.get_client_by_id(client_id)

        if client is None:
            log.warning("No found client by id")
            return jsonify({"warning": "Client dont exist. Try again"}), 404

        parking: Parking = Parking.get_parking_by_id(parking_id)

        if parking is None:
            log.warning("No found parking by id")
            return jsonify({"warning": "Parking dont exist. Try again"}), 404

        is_opened_parking: Parking = Parking.is_open(parking_id)

        if is_opened_parking:

            is_available_places = Parking.is_available_places(parking_id)

            if is_available_places:

                new_client_parking = ClientParking(
                    client_id=client_id,
                    parking_id=parking_id,
                    time_in=datetime.now()
                )
                db.session.add(new_client_parking)
                Parking.update_parking_places(parking_id, False)
                db.session.commit()
                return f"Successfully added client_parking", 201

            else:
                return jsonify({"info": "Parking hasn't available places - come back later"}), 200

        else:
            return jsonify({"info": "Parking is closed - come back later"}), 200

    except Exception as e:
        log.exception("Something went wrong while adding client_parking", exc_info=e)
        return jsonify({"exception": "Something went wrong"}), 404


@bp.route('/client_parkings', methods=['DELETE'])
def delete_client_parking():
    try:
        data = request.get_json()

        client_id = data["client_id"]
        parking_id = data["parking_id"]

        client_parking: ClientParking = ClientParking.get_client_parking_by_id(
            client_id, parking_id
        )
        """ проверка есть ли на парковке сейчас такой клиент """
        if client_parking:
            card_number = Client.get_client_card(client_id)
            """ отпустить клиента с парковки можно только если у него карта привязана """
            if card_number:
                """ добавляем в сессию вставку записи о клиенте в историю """
                new_client_parking_log = ClientParkingLog(
                    client_id=client_parking.client_id,
                    parking_id=client_parking.parking_id,
                    time_in=client_parking.time_in,
                    time_out=datetime.now()
                )
                db.session.add(new_client_parking_log)
                """ добавляем в сессию удаление записи о клиенте из таблицы с текущими машинами на парковке """
                db.session.delete(client_parking)  # удаляем запись
                """ Клиент уезжает - одно место освободилось - освобождаем место """
                Parking.update_parking_places(parking_id, True)
                """ все изменения фиксируются в базе - в случае какой-либо ошибки - все откатится """
                db.session.commit()
                return jsonify({"info": "Successfully delete client_parking"}), 201

            else:
                return jsonify({"info": "No money - no honey"}), 200

        else:
            log.warning("Not find client_parking")
            return jsonify({"warning": "Client_parking dont exist. Try again"}), 404

    except Exception as e:
        log.exception("Something went wrong while deleting client_parking", exc_info=e)
        return jsonify({"exception": "Something went wrong"}), 404
