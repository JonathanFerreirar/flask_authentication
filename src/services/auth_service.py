from models.users_model import User
from models.auth_model import TokenBlocklist

from infra.database import get_database_session

from utils.extentions import bcrypt, jwt
from utils.validations import login_validations, user_validations

from flask_jwt_extended import create_access_token, get_jwt

from erros import ERRO_NOT_FOUND_USER, ERRO__INVALID_EMAIL_OR_PASSWORD, ERRO_ALREDY_EXIST_USER


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]

    with get_database_session() as database:
        token = database.query(TokenBlocklist).filter_by(jti=jti).first()

        return token is not None


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data["sub"]
    with get_database_session() as database:

        user = database.query(User).filter_by(email=identity).first()
        database.close()

        return user.to_dict()


def login_user(data):
    try:
        with get_database_session() as database:

            validation_error = login_validations(data)
            if validation_error:
                return validation_error

            user = database.query(User).filter_by(email=data['email']).first()
            database.close()

            if not user:
                return ERRO_NOT_FOUND_USER

            isCorrectPassword = bcrypt.check_password_hash(
                user.password, data['password'])

            if isCorrectPassword:

                access_token = create_access_token(identity=user.email)

                return {
                    "data": {
                        **user.to_dict(),
                        "access_token": access_token
                    }
                }, 200

            return ERRO__INVALID_EMAIL_OR_PASSWORD

    except Exception as e:
        return {"error": str(e)}, 500


def create_new_user(data):
    validation_error = user_validations(data)

    if validation_error:
        return validation_error
    try:
        with get_database_session() as database:
            user = database.query(User).filter_by(email=data['email']).first()
            if user:
                return ERRO_ALREDY_EXIST_USER

            hashed_password = bcrypt.generate_password_hash(
                data['password']).decode('utf-8')

            new_user = User(name=data['name'],
                            password=hashed_password, email=data['email'])

            database.add(new_user)
            database.flush()
            database.refresh(new_user)

            access_token = create_access_token(identity=new_user.id)

            return {
                "data": {
                    **new_user.to_dict(),
                    "access_token": access_token
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def logout_user():
    jti = get_jwt()["jti"]

    with get_database_session() as database:
        database.add(TokenBlocklist(jti=jti))

        return {
            "data": {
                "msg": "token revoked"
            }
        }, 200
