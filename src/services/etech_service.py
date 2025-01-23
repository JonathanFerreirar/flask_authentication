from models.etechs_model import Etech
from infra.database import get_database_session

from utils.validations import etech_validations


def create_new_etech(data):
    validation_error = etech_validations(data)

    if validation_error:
        return validation_error
    try:
        with get_database_session() as database:

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
