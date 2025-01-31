from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from services.content_service import create_new_content, get_content_by_id, get_all_content_from_chapter, update_content


content_bp = Blueprint('content', __name__)


@content_bp.route('/',  methods=['POST'])
@jwt_required()
def create_content():
    body = request.get_json()

    result, status = create_new_content(body)

    return jsonify(result), status


@content_bp.route('/<int:content_id>',  methods=['GET'])
@content_bp.route('/', defaults={'content_id': None}, methods=['GET'])
@jwt_required()
def get_content(content_id):

    chapter_id = request.args.get('chapter')

    if chapter_id:
        result, status = get_all_content_from_chapter(chapter_id)

        return jsonify(result), status

    result, status = get_content_by_id(content_id)

    return jsonify(result), status


@content_bp.route('/<int:content_id>',  methods=['PUT'])
@jwt_required()
def update_cotent_router(content_id):
    body = request.get_json()

    if request.method == 'PUT':
        result, status = update_content(body, content_id)

        return jsonify(result), status
