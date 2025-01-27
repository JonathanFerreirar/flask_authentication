from models.chapter_model import Chapter
from models.etechs_model import Etech
from infra.database import get_database_session

from utils.validations import chapter_validations, update_chapter_valitaions

from erros import ERRO_NOT_FOUND_CHAPTER, ERRO_MISS_BODY

from erros import ERRO_UNAUTHORIZED_USER, ERRO_NOT_FOUND_CHAPTER, ERRO_BAD_REQUEST_CHAPTER, ERRO_ALREDY_EXIST_THIS_CHAPTER

from dtos.chapter import ChapterCreateDTO, ChapterUpdateDTO
from flask_jwt_extended import jwt_required, get_current_user


def create_new_chapter(data: ChapterCreateDTO):
    user = get_current_user()

    current_user = user['id']

    validation_error = chapter_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            title = database.query(Chapter).filter_by(
                title=data['title'], etech=data['etech']).first()
            if title:
                return ERRO_ALREDY_EXIST_THIS_CHAPTER

            chapter_number = database.query(Chapter).filter_by(
                chapter_number=data['chapter_number'], etech=data['etech']).first()
            if chapter_number:
                return ERRO_ALREDY_EXIST_THIS_CHAPTER

            etech = database.query(Etech).filter_by(
                id=data['etech']).first()

            if not etech or etech.user != current_user:
                return ERRO_UNAUTHORIZED_USER

            new_chapter = Chapter(
                title=data['title'], etech=data['etech'], chapter_number=data['chapter_number'])

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
                return ERRO_NOT_FOUND_CHAPTER

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
                return ERRO_NOT_FOUND_CHAPTER

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

    try:
        with get_database_session() as database:
            chapter = database.query(Chapter).filter_by(
                id=chapter_id).first()

            if "title" in data:
                filtered_by_title = database.query(Chapter).filter_by(
                    title=data['title']).first()
                if filtered_by_title:
                    return ERRO_ALREDY_EXIST_THIS_CHAPTER

            for key, value in data.items():
                match key:
                    case 'title':
                        chapter.title = value

                    case _:
                        return ERRO_BAD_REQUEST_CHAPTER

            database.flush()
            database.refresh(chapter)

            return {
                "data": {
                    **chapter.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
