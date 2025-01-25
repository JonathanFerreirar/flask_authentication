from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_current_user
from services.etech_service import create_new_etech, get_etech_by_id, get_all_etechs, update_etech


etech_bp = Blueprint('etech', __name__)


@etech_bp.route('/create',  methods=['POST'])
@jwt_required()
def create_etech():
    body = request.get_json()

    user = get_current_user()

    if body['user'] != user['id']:
        return ERRO_UNAUTHORIZED_USER

    result, status = create_new_etech(body)

    return jsonify(result), status


@etech_bp.route('/<int:etech_id>',  methods=['GET'])
@etech_bp.route('/', defaults={'etech_id': None}, methods=['GET'])
def get_etech(etech_id):

    if not etech_id:
        result, status = get_all_etechs()

        return jsonify(result), status

    result, status = get_etech_by_id(etech_id)

    return jsonify(result), status


@etech_bp.route('/update/<int:etech_id>',  methods=['PUT'])
@jwt_required()
def update_etech_router(etech_id):
    body = request.get_json()

    if request.method == 'PUT':
        result, status = update_etech(body, etech_id)

        return jsonify(result), status
