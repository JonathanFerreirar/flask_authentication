from models.user_model import User
from infra.database import get_database_session

from erros import ERRO_NOT_FOUND_USER

erro__not_found, erro_status_not_found, = ERRO_NOT_FOUND_USER


def get_all_users():
    try:
        with get_database_session() as database:
            users = database.query(User).all()
            return [user.to_dict() for user in users]

    except Exception as e:
        return {"error": str(e)}, 500


def get_user_by_id(user_id):
    try:
        with get_database_session() as database:

            user = database.get(User, user_id)
            database.close()

            if not user:
                return {"error": erro__not_found['erro'], "message": erro__not_found['message']}, erro_status_not_found

            return {"data": user.to_dict()}, 200

    except Exception as e:
        return {"error": str(e)}, 500


def delete_user_by_id(user_id):
    try:
        with get_database_session() as database:

            user = database.query(User).filter(User.id == user_id).first()

            if user:
                database.delete(user)
                return {}, 204
            else:
                return {
                    "error": erro__not_found['erro'], "message": erro__not_found['message']
                }, erro_status_not_found

    except Exception as e:
        return {"error": str(e)}, 500
