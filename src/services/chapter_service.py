from models.etechs_model import Etech
from models.chapters_model import Chapter
from infra.database import get_database_session

from flask_jwt_extended import get_current_user
from dtos.chapter import ChapterCreateDTO, ChapterUpdateDTO

from utils.validations import chapter_validations, update_chapter_valitaions

from erros import ERRO_UNAUTHORIZED_USER
from erros import ERRO_NOT_FOUND, ERRO_ALREDY_EXIST, ERRO_BAD_REQUEST, ERRO_MISS_BODY

from sqlalchemy.orm import Session
from sqlalchemy import desc


def get_last_chapter(database: Session, etech: int):

    last_chapter = database.query(Chapter).filter(Chapter.etech == etech).order_by(
        desc(Chapter.chapter_number)
    ).first()

    return {
        "chapter_number": last_chapter.chapter_number if last_chapter else 0
    }


def create_new_chapter(data: ChapterCreateDTO):
    user = get_current_user()

    current_user = user['id']

    validation_error = chapter_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            last_chapter = get_last_chapter(database, data['etech'])

            new_chapter_number = last_chapter['chapter_number'] + 1

            title = database.query(Chapter).filter_by(
                title=data['title'], etech=data['etech']).first()
            if title:
                return ERRO_ALREDY_EXIST('chapter')

            etech = database.query(Etech).filter_by(
                id=data['etech']).first()

            if not etech or etech.user != current_user:
                return ERRO_UNAUTHORIZED_USER

            new_chapter = Chapter(
                title=data['title'], etech=data['etech'], chapter_number=new_chapter_number)

            database.add(new_chapter)
            database.flush()
            database.refresh(new_chapter)

            return {
                "data": {
                    **new_chapter.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_chapter_by_id(chapter_id):
    try:
        with get_database_session() as database:

            chapter = database.get(Chapter, chapter_id)

            if not chapter:
                return ERRO_NOT_FOUND('chapter')

            return {"data": {
                **chapter.to_dict()
            }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_all_chapter_from_user(etech_id):
    try:
        with get_database_session() as database:
            chapters = database.query(Chapter).filter_by(
                etech=etech_id).all()

            if not chapters:
                return {
                    "data": []
                }, 200

            return {
                "data": [chapter.to_dict() for chapter in chapters]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def update_chapter(data: ChapterUpdateDTO, chapter_id):
    if not data:
        return ERRO_MISS_BODY

    validation_error = update_chapter_valitaions(data)
    if validation_error:
        return validation_error

    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:
            chapter = database.query(Chapter).filter_by(
                id=chapter_id).first()

            etech_user_id = chapter.to_dict_with_etech().get(
                'etech', {}).get('user', {}).get('id')

            if etech_user_id != current_user:
                return ERRO_UNAUTHORIZED_USER

            if "title" in data:
                filtered_by_title = database.query(Chapter).filter_by(
                    title=data['title']).first()
                if filtered_by_title:
                    return ERRO_ALREDY_EXIST('chapter')

            for key, value in data.items():
                match key:
                    case 'title':
                        chapter.title = value

                    case _:
                        return ERRO_BAD_REQUEST

            database.flush()
            database.refresh(chapter)

            return {
                "data": {
                    **chapter.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
