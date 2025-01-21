from utils.validations import user_validations
from models.user_model import User
from infra.database import get_database_session


def get_all_users():
    try:
        with get_database_session() as database:
            users = database.query(User).all()
            return [user.to_dict() for user in users]

    except Exception as e:
        return {"error": str(e)}, 500


def create_new_user(data):
    validation_error = user_validations(data)

    if validation_error:
        return validation_error
    try:
        with get_database_session() as database:

            new_user = User(name=data['name'],
                            password=data['password'], email=data['email'])

            database.add(new_user)

            return {"data": new_user.to_dict()}, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_user_by_id(user_id):
    try:
        with get_database_session() as database:

            user = database.get(User, user_id)
            database.close()

            if not user:
                return {"error": "Usuário não encontrado."}, 404

            return {"data": user.to_dict()}, 200

    except Exception as e:
        return {"error": str(e)}, 500
