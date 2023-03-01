from flask import Blueprint, jsonify, request

from module_29_testing.hw.flaskr.models import Parking
from module_29_testing.hw.flaskr import db
from module_29_testing.hw.flaskr.log import log

bp = Blueprint('parkings', __name__)


@bp.route('/parkings', methods=['POST'])
def add_parking():
    try:
        data = request.get_json()

        address = data["address"]
        opened = data["opened"]
        count_places = data["count_places"]
        count_available_places = data["count_available_places"]

        # coffee_id = get_coffee_id(coffee)

        # if coffee_id:
        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places
        )
        db.session.add(new_parking)
        db.session.commit()
        return f"Successfully added parking", 201
        # else:
        #     return f"Coffee dont exist. Try again", 202

    except Exception as e:
        log.exception("Something went wrong while adding parking", exc_info=e)
        return jsonify({"exception": "Something went wrong"}), 404
