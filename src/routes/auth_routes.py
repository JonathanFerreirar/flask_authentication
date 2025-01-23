from flask import jsonify, request, Blueprint
from services.auth_service import login_user, create_new_user


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login',  methods=['POST'])
def users():
    body = request.get_json()

    result, status = login_user(body)

    return jsonify(result), status


@auth_bp.route('/create-user',  methods=['POST'])
def create_user():
    body = request.get_json()

    result, status = create_new_user(body)

    return jsonify(result), status
