from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from services.chapter_service import create_new_chapter, get_chapter_by_id, get_all_chapter_from_user, update_chapter


chapter_bp = Blueprint('chapter', __name__)


@chapter_bp.route('/',  methods=['POST'])
@jwt_required()
def create_etech():
    body = request.get_json()

    result, status = create_new_chapter(body)

    return jsonify(result), status


@chapter_bp.route('/<int:chapter_id>',  methods=['GET'])
@chapter_bp.route('/', defaults={'chapter_id': None}, methods=['GET'])
@jwt_required()
def get_etech(chapter_id):

    etech_id = request.args.get('etech')

    if etech_id:
        result, status = get_all_chapter_from_user(etech_id)

        return jsonify(result), status

    result, status = get_chapter_by_id(chapter_id)

    return jsonify(result), status


@chapter_bp.route('/<int:chapter_id>',  methods=['PUT'])
@jwt_required()
def update_etech_router(chapter_id):
    body = request.get_json()

    if request.method == 'PUT':
        result, status = update_chapter(body, chapter_id)

        return jsonify(result), status
