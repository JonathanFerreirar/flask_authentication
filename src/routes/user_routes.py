from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_current_user
from services.user_service import get_all_users, delete_user_by_id


user_bp = Blueprint('user', __name__)


@user_bp.route('/',  methods=['GET'])
@jwt_required()
def users():
    result, status = get_all_users()

    return jsonify(result), status


@user_bp.route('/<int:user_id>', methods=['GET', 'DELETE'])
@jwt_required()
def get_user(user_id):
    user = get_current_user()

    if user_id != user['id']:
        return ERRO_UNAUTHORIZED_USER

    if request.method == 'DELETE':
        result, status = delete_user_by_id(user_id)

        return jsonify(result), status

    return jsonify({
        "data": user
    }), 200
