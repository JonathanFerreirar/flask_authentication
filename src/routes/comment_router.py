from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from services.comment_service import create_new_comment, get_all_comment_from_etech, get_comment_by_id, update_comment


comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/',  methods=['POST'])
@jwt_required()
def create_comment():
    body = request.get_json()

    result, status = create_new_comment(body)

    return jsonify(result), status


@comment_bp.route('/<int:content_id>',  methods=['GET'])
@comment_bp.route('/', defaults={'content_id': None}, methods=['GET'])
def get_comments_by_etech(content_id):

    etech_id = request.args.get('etech')

    if etech_id:
        result, status = get_all_comment_from_etech(etech_id)

        return jsonify(result), status

    result, status = get_comment_by_id(content_id)

    return jsonify(result), status


@comment_bp.route('/<int:content_id>',  methods=['PUT'])
@jwt_required()
def update_comment_router(content_id):
    body = request.get_json()

    if request.method == 'PUT':
        result, status = update_comment(body, content_id)

        return jsonify(result), status
