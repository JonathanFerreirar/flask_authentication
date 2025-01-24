from models.etechs_model import Etech
from infra.database import get_database_session

from utils.validations import etech_validations

from erros import ERRO_ALREDY_EXIST_TITLE, ERRO_ALREDY_EXIST_DESCRIPTION, ERRO_NOT_FOUND_ETECH


def create_new_etech(data):
    validation_error = etech_validations(data)

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            title = database.query(Etech).filter_by(
                title=data['title']).first()
            if title:
                return ERRO_ALREDY_EXIST_TITLE

            description = database.query(Etech).filter_by(
                description=data['description']).first()

            if description:
                return ERRO_ALREDY_EXIST_DESCRIPTION

            new_etech = Etech(user=data['user'], price=data['price'], image=data['image'],
                              title=data['title'], topics=data['topics'], description=data['description'])

            database.add(new_etech)
            database.flush()
            database.refresh(new_etech)

            return {
                "data": {
                    **new_etech.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500


def get_etech_by_id(etech_id):
    try:
        with get_database_session() as database:

            etech = database.get(Etech, etech_id)

            if not etech:
                return ERRO_NOT_FOUND_ETECH

            return {"data": {
                **etech.to_dict()
            }
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def get_all_etechs():
    try:
        with get_database_session() as database:
            etechs = database.query(Etech).all()
            return {
                "data": [etech.to_dict() for etech in etechs]
            }, 200

    except Exception as e:
        return {"error": str(e)}, 500


def update_etech(data):
    try:
        with get_database_session() as database:

            title = database.query(Etech).filter_by(
                title=data['title']).first()
            if title:
                return ERRO_ALREDY_EXIST_TITLE

            description = database.query(Etech).filter_by(
                description=data['description']).first()

            if description:
                return ERRO_ALREDY_EXIST_DESCRIPTION

            # updated_etech = Etech(user=data['user'], price=data['price'], image=data['image'],
             #                 title=data['title'], topics=data['topics'], description=data['description'])
            updated_etech = {

                "title": "Factory teeeee",
                "description":
                "Aoobaaa."
            }
            database.update(title='Factory teeeee')
            database.flush()
            database.refresh(updated_etech)

            return {
                "data": {
                    **updated_etech.to_dict(),
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
