from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from services.profile_service import create_new_profile, update_profile, get_profile_by_id, get_all_profiles


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/',  methods=['POST'])
@jwt_required()
def create_profile():
    body = request.get_json()

    result, status = create_new_profile(body)

    return jsonify(result), status


@profile_bp.route('/<int:profile_id>',  methods=['PUT'])
@jwt_required()
def update_etech_router(profile_id):
    body = request.get_json()

    if request.method == 'PUT':
        result, status = update_profile(body, profile_id)

        return jsonify(result), status

#


@profile_bp.route('/<int:profile_id>',  methods=['GET'])
@profile_bp.route('/', defaults={'profile_id': None}, methods=['GET'])
@jwt_required()
def get_etech(profile_id):

    if not profile_id:
        result, status = get_all_profiles()

        return jsonify(result), status

    result, status = get_profile_by_id(profile_id)

    return jsonify(result), status
