from models.etechs_model import Etech
from models.comments_model import Comment
from infra.database import get_database_session


from dtos.comment import CommentDTO
from flask_jwt_extended import get_current_user
from utils.validations import comment_validations, update_comment_valitaions

from erros import ERRO_MISS_BODY, ERRO_BAD_REQUEST
from erros import ERRO_UNAUTHORIZED_USER, ERRO_NOT_FOUND


def create_new_comment(data: CommentDTO):
    user = get_current_user()

    current_user = user['id']

    validation_error = comment_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:
            exist_etech = database.query(
                Etech).filter_by(id=data['etech']).first()

            if not exist_etech:
                return ERRO_NOT_FOUND('etech')

            new_comment = Comment(
                user=current_user, etech=data['etech'], comment=data['comment'])

            database.add(new_comment)
            database.flush()
            database.refresh(new_comment)

            return {
                "data": {
                    **new_comment.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_comment_by_id(comment_id):
    try:
        with get_database_session() as database:

            comment = database.get(Comment, comment_id)

            if not comment:
                return ERRO_NOT_FOUND('comment')

            return {"data": {
                **comment.to_dict()
            }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_all_comment_from_etech(etech_id):
    try:
        with get_database_session() as database:
            comments = database.query(Comment).filter_by(
                etech=etech_id).all()

            if not comments:
                return ERRO_NOT_FOUND('comment')

            return {
                "data": [comment.to_dict() for comment in comments]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def update_comment(data: CommentDTO, comment_id):
    if not data:
        return ERRO_MISS_BODY

    validation_error = update_comment_valitaions(data)
    if validation_error:
        return validation_error

    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:
            comment = database.query(Comment).filter_by(
                id=comment_id).first()

            if not comment:
                return ERRO_NOT_FOUND('comment')

            if comment.user != current_user:
                return ERRO_UNAUTHORIZED_USER

            for key, value in data.items():
                match key:
                    case 'comment':
                        comment.comment = value

                    case _:
                        return ERRO_BAD_REQUEST

            database.flush()
            database.refresh(comment)

            return {
                "data": {
                    **comment.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
