from models.chapters_model import Chapter
from models.contents_model import Content
from infra.database import get_database_session


from flask_jwt_extended import get_current_user
from dtos.content import ContentCreateDTO, ContentUpdateDTO
from utils.validations import content_validations, update_content_valitaions

from erros import ERRO_MISS_BODY, ERRO_BAD_REQUEST
from erros import ERRO_UNAUTHORIZED_USER, ERRO_NOT_FOUND, ERRO_ALREDY_EXIST


def create_new_content(data: ContentCreateDTO):
    user = get_current_user()

    current_user = user['id']

    validation_error = content_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            page = database.query(Content).filter_by(
                page=data['page'], chapter=data['chapter']).first()
            if page:
                return ERRO_ALREDY_EXIST('content')

            chapter = database.query(Chapter).filter_by(
                id=data['chapter']).first()

            if not chapter:
                return ERRO_NOT_FOUND('chapter')

            etech_user_id = chapter.to_dict_with_etech().get(
                'etech', {}).get('user', {}).get('id')

            if etech_user_id != current_user:
                return ERRO_UNAUTHORIZED_USER

            images = data.get('images')

            new_content = Content(
                chapter=data['chapter'], content=data['content'], page=data['page'], images=images)

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


def update_content(data: ContentUpdateDTO, content_id):
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
                    case 'content':
                        content.content = value

                    case 'images':
                        content.images = value

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
