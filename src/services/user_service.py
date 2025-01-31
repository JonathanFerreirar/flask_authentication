from models.users_model import User
from infra.database import get_database_session

from erros import ERRO_NOT_FOUND


def get_all_users():
    try:
        with get_database_session() as database:
            users = database.query(User).all()
            return {
                "data": [user.to_dict() for user in users]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_user_by_id(user_id):
    try:
        with get_database_session() as database:

            user = database.get(User, user_id)
            database.close()

            if not user:
                return ERRO_NOT_FOUND('user')

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
                return ERRO_NOT_FOUND('user')

    except Exception as e:
        return {"error": str(e)}, 500
