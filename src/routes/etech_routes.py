from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_current_user
from services.etech_service import create_new_etech


etech_bp = Blueprint('etech', __name__)


@jwt_required()
@etech_bp.route('/create',  methods=['POST'])
def create_user():
    body = request.get_json()

    result, status = create_new_etech(body)

    return jsonify(result), status
