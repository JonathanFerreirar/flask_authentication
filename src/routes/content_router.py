import re

from erros import ERRO_UNAUTHORIZED_USER

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from services.content_service import create_new_content, get_content_by_id, get_all_content_from_chapter, update_content, get_contents_quantity_by_chapter, get_content_by_page_and_chapter


content_bp = Blueprint('content', __name__)


@content_bp.route('/',  methods=['POST'])
@jwt_required()
def create_content():

    title = request.form.get('title')
    content = request.form.get('content')
    chapter = request.form.get('chapter')

    files = request.files
    images = []

    for index, img in enumerate(files.values()):
        img_name = request.form.get(f'name-{index}')
        image_obj = {
            "image": img,
            "name": img_name
        }
        images.append(image_obj)

    data = {
        key: value
        for key, value in {
            "title": title,
            "images": images,
            "content": content,
            "chapter": chapter,
        }.items()
        if value is not None
    }

    result, status = create_new_content(data)

    return jsonify(result), status


@content_bp.route('/<int:content_id>',  methods=['GET'])
@content_bp.route('/', defaults={'content_id': None}, methods=['GET'])
@jwt_required()
def get_content(content_id):

    chapter_id = request.args.get('chapter')
    page = request.args.get('page')

    if chapter_id and page:
        result, status = get_content_by_page_and_chapter(
            chapter_id=chapter_id, page=page)

        return jsonify(result), status

    if chapter_id and not page:
        result, status = get_all_content_from_chapter(chapter_id)

        return jsonify(result), status

    result, status = get_content_by_id(content_id)

    return jsonify(result), status


@content_bp.route('/<int:content_id>',  methods=['PUT'])
@jwt_required()
def update_cotent_router(content_id):

    title = request.form.get('title')
    content = request.form.get('content')

    files = request.files
    images = []

    print("FILEEEEEEEEEEESSSSSSSSSSS", files)

    for key, img in files.items():
        
        match = re.search(r'\d+', key)
        file_index = match.group() if match else None 
        
        img_name = request.form.get(f'name-{file_index}')
        img_id = request.form.get(f'id-{file_index}')

        image_obj = {
            "id": img_id,
            "image": img,
            "name": img_name
        }
        
        images.append(image_obj)

    data = {
        key: value
        for key, value in {
            "title": title,
            "images": images,
            "content": content,
        }.items()
        if value is not None
    }

    if request.method == 'PUT':

        result, status = update_content(data, content_id)

        return jsonify(result), status


@content_bp.route('/quantity-by-chapter', methods=['GET'])
@jwt_required()
def get_quantity_by_chapter():
    chapter_id = request.args.get('chapter')

    if chapter_id:
        result, status = get_contents_quantity_by_chapter(chapter_id)

        return jsonify(result), status
