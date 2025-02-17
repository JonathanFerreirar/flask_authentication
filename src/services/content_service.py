import json

from models.chapters_model import Chapter
from models.contents_model import Content
from infra.database import get_database_session
from infra.cloudinary import CloudinaryUploader


from flask_jwt_extended import get_current_user
from dtos.content import ContentCreateDTO, ContentUpdateDTO
from utils.validations import content_validations, update_content_valitaions

from erros import ERRO_MISS_BODY, ERRO_BAD_REQUEST, ERRO_UPLOAD_FILE
from erros import ERRO_UNAUTHORIZED_USER, ERRO_NOT_FOUND, ERRO_ALREDY_EXIST

from sqlalchemy import desc
from sqlalchemy.orm import Session

from utils import generate_random_value


def get_last_page(database: Session, chapter: int):

    last_chapter = database.query(Content).filter(Content.chapter == chapter).order_by(
        desc(Content.page)
    ).first()

    return {
        "page": last_chapter.page if last_chapter else 0
    }


def create_new_content(data: ContentCreateDTO):
    user = get_current_user()
    upload_file = CloudinaryUploader()

    current_user = user['id']

    validation_error = content_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            last_page = get_last_page(database, data['chapter'])

            new_page_number = last_page['page'] + 1

            page = database.query(Content).filter_by(
                page=new_page_number, chapter=data['chapter']).first()
            if page:
                return ERRO_ALREDY_EXIST('page')

            chapter = database.query(Chapter).filter_by(
                id=data['chapter']).first()

            if not chapter:
                return ERRO_NOT_FOUND('chapter')

            etech_user_id = chapter.to_dict_with_etech().get(
                'etech', {}).get('user', {}).get('id')

            if etech_user_id != current_user:
                return ERRO_UNAUTHORIZED_USER

            images = data.get('images')

            files = []

            for file_obj in images:

                url_file = upload_file.upload_file(
                    file_obj['image'], public_id=new_page_number, asset_folder='contents')

                if not url_file['success']:
                    return ERRO_UPLOAD_FILE

                url_response = url_file['secure_url']
                url_response_id = url_file['id']

                image_obj = {
                    "id": url_response_id,
                    "image": url_response,
                    "name": file_obj['name']
                }

                files.append(json.dumps(image_obj))

            title = data.get('title')

            new_content = Content(
                chapter=data['chapter'], content=data['content'], title=title, page=new_page_number, images=files)

            database.add(new_content)
            database.flush()
            database.refresh(new_content)

            return {
                "data": {
                    **new_content.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_content_by_id(content_id):
    try:
        with get_database_session() as database:

            content = database.get(Content, content_id)

            if not content:
                return ERRO_NOT_FOUND('chapter')

            return {"data": {
                **content.to_dict()
            }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_all_content_from_chapter(chapter_id):
    try:
        with get_database_session() as database:
            contents = database.query(Content).filter_by(
                chapter=chapter_id).all()

            if not contents:
                return ERRO_NOT_FOUND('chapter')

            return {
                "data": [chapter.to_dict() for chapter in contents]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_contents_quantity_by_chapter(chapter_id):
    try:
        with get_database_session() as database:
            contents = database.query(Content).filter_by(
                chapter=chapter_id).count()

            return {
                "data": contents
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_content_by_page_and_chapter(chapter_id, page):
    try:
        with get_database_session() as database:
            content = database.query(Content).filter_by(
                chapter=chapter_id, page=page).first()

            if not content:
                return ERRO_NOT_FOUND("content")

            return {
                "data": {
                    **content.to_dict()
                }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def update_content(data: ContentUpdateDTO, content_id):
    upload_file = CloudinaryUploader()

    if not data:
        return ERRO_MISS_BODY

    validation_error = update_content_valitaions(data)
    if validation_error:
        return validation_error

    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:
            content = database.query(Content).filter_by(
                id=content_id).first()

            chapter = content.to_dict_with_chapter()

            
            if not chapter:
                return ERRO_NOT_FOUND('chapter')

            etech_user_id = chapter.get('chapter', {}).get(
                'etech', {}).get('user', {}).get('id')

            if etech_user_id != current_user:
                return ERRO_UNAUTHORIZED_USER

            for key, value in data.items():
                match key:
                    case 'title':
                        content.title = value

                    case 'content':
                        content.content = value

                    case 'images':
                        
                        actual_images = content.images
                        files = [*actual_images]

                        for file_obj in value:
                            img_id = file_obj['id']
                            url_file = None

                            if img_id:
                        
                                existing_file_index = next(
                                    (index for index, file in enumerate(files) if json.loads(file)['id'] == img_id),
                                    None
                                )

                                
                                url_file = upload_file.update_file(
                                    file_obj['image'], public_id=img_id, asset_folder='contents'
                                )

                                if not url_file['success']:
                                    return ERRO_UPLOAD_FILE

                                url_response = url_file['secure_url']
                                url_response_id = url_file['id']

                                updated_image_obj = {
                                    "id": url_response_id,
                                    "image": url_response,
                                    "name": file_obj['name']
                                }

        
                                if existing_file_index is not None:
                                    files[existing_file_index] = json.dumps(updated_image_obj)
                            else:
                                
                                random_value = generate_random_value(1, 999)

                                url_file = upload_file.upload_file(
                                    file_obj['image'], public_id=random_value, asset_folder='contents'
                                )

                                if not url_file['success']:
                                    return ERRO_UPLOAD_FILE

                                url_response = url_file['secure_url']
                                url_response_id = url_file['id']

                                new_image_obj = {
                                    "id": url_response_id,
                                    "image": url_response,
                                    "name": file_obj['name']
                                }

                                files.append(json.dumps(new_image_obj))

                        
                        content.images = files
                        break
                        

                    case _:
                        return ERRO_BAD_REQUEST

            database.flush()
            database.refresh(content)

            return {
                "data": {
                    **content.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
