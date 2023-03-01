from typing import List

from flask import Blueprint, jsonify, request

from module_29_testing.hw.flaskr.models import Client
from module_29_testing.hw.flaskr import db
from module_29_testing.hw.flaskr.log import log

bp = Blueprint('clients', __name__)


@bp.route('/clients', methods=['POST'])
def add_client():
    try:
        data = request.get_json()

        name = data["name"]
        surname = data["surname"]
        credit_card = data["credit_card"]
        car_number = data["car_number"]

        # coffee_id = get_coffee_id(coffee)

        # if coffee_id:
        new_client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number
        )
        db.session.add(new_client)
        db.session.commit()
        return f"Successfully added user", 201
        # else:
        #     return f"Coffee dont exist. Try again", 202

    except Exception as e:
        log.exception("Something went wrong while adding client", exc_info=e)
        return jsonify({"exception": "Something went wrong"}), 404


@bp.route('/clients', methods=['GET'])
def get_clients():

    clients: List[Client] = db.session.query(Client).all()

    if clients:
        client_list = []
        for client in clients:
            client_list.append(client.to_json())
        return jsonify(client_list=client_list), 200
    else:
        log.warning("No clients")
        return jsonify({"warning": "Clients dont exist. Table of Clients is empty"}), 404


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id: int):

    client: Client = Client.get_client_by_id(client_id)

    if client:
        return jsonify(client.to_json()), 200
    else:
        log.warning("No client by id")
        return jsonify({"warning": "Client dont exist. Try again"}), 404
