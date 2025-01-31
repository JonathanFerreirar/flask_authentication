from models.profile_model import Profile
from flask_jwt_extended import get_current_user
from infra.database import get_database_session

from utils.string import remove_space
from utils.validations import update_profile_valitaions


from erros import ERRO_ALREDY_EXIST, ERRO_MISS_BODY, ERRO_BAD_REQUEST, ERRO_UNAUTHORIZED_USER, ERRO_NOT_FOUND


def create_new_profile(data):
    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:

            profile = database.query(Profile).filter_by(
                user=current_user).first()

            if profile:
                return ERRO_ALREDY_EXIST('profile')

            new_profile = Profile(
                user=current_user, description=data['description'], image=data['image'])

            database.add(new_profile)
            database.flush()
            database.refresh(new_profile)

            return {
                "data": {
                    **new_profile.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def update_profile(data, profile_id):
    if not data:
        return ERRO_MISS_BODY

    validation_error = update_profile_valitaions(data)
    if validation_error:
        return validation_error

    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:
            profile = database.query(Profile).filter_by(
                id=profile_id).first()

            if current_user != profile.user:
                return ERRO_UNAUTHORIZED_USER

            for key, value in data.items():
                match key:
                    case 'description':
                        value_trated = remove_space(value)
                        if value_trated:
                            profile.description = value
                    case 'image':
                        value_trated = remove_space(value)
                        if value_trated:
                            profile.image = value
                    case _:
                        return ERRO_BAD_REQUEST

            database.flush()
            database.refresh(profile)

            return {
                "data": {
                    **profile.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_profile_by_id(profile_id):
    user = get_current_user()

    current_user = user['id']

    try:
        with get_database_session() as database:

            profile = database.get(Profile, profile_id)

            if not profile:
                return ERRO_NOT_FOUND('profile')

            if current_user != profile.user:
                return ERRO_UNAUTHORIZED_USER

            return {"data": {
                **profile.to_dict()
            }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_all_profiles():
    try:
        with get_database_session() as database:
            profiles = database.query(Profile).all()
            return {
                "data": [profile.to_dict() for profile in profiles]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500
