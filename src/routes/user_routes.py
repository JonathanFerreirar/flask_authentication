from flask import jsonify, request, Blueprint
from services.user_service import get_all_users, create_new_user, get_user_by_id, delete_user_by_id


user_bp = Blueprint('user', __name__)


@user_bp.route('/',  methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        body = request.get_json()
        result, status = create_new_user(body)

        return jsonify(result), status

    users = get_all_users()
    return jsonify({"data": users}), 200


@user_bp.route('/<int:user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    if request.method == 'DELETE':
        result, status = delete_user_by_id(user_id)

        return jsonify(result), status

    result, status = get_user_by_id(user_id)

    return jsonify(result), status
