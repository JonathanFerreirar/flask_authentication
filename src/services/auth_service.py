from models.user_model import User
from utils.extentions import bcrypt
from infra.database import get_database_session
from utils.validations import login_validations

from flask_jwt_extended import create_access_token


def login_user(data):
    try:
        with get_database_session() as database:

            validation_error = login_validations(data)
            if validation_error:
                return validation_error

            user = database.query(User).filter_by(email=data['email']).first()
            database.close()

            if not user:
                return {"error": "not Found", "message": "user not found"}, 404

            isCorrectPassword = bcrypt.check_password_hash(
                user.password, data['password'])

            if isCorrectPassword:

                access_token = create_access_token(identity=user.name)

                return {
                    "data": {
                        **user.to_dict(),
                        "access_token": access_token
                    }
                }, 200

            return {"error": "Unauthorized",
                    "message": "Invalid email or password."}, 400

    except Exception as e:
        return {"error": str(e)}, 500
