import json

from models.etechs_model import Etech
from infra.cloudinary import CloudinaryUploader
from infra.database import get_database_session

from dtos.etech import EtechUpdateDTO
from flask_jwt_extended import get_current_user
from utils.validations import etech_validations, update_etech_valitaions


from erros import ERRO_MISS_BODY, ERRO_BAD_REQUEST, ERRO_ALREDY_EXIST, ERRO_NOT_FOUND, ERRO_UPLOAD_FILE


def create_new_etech(request):
    price = request.form.get('price')
    topics = request.form.get('topics')
    title_form = request.form.get('title')
    language = request.form.get('language')
    description_form = request.form.get('description')

    if topics:
        try:
            topics = json.loads(topics)
        except json.JSONDecodeError:
            topics = None

    data = {
        key: value
        for key, value in {
            "price": price,
            "topics": topics,
            "title": title_form,
            "language": language,
            "description": description_form,
        }.items()
        if value is not None
    }

    validation_error = etech_validations(data)

    user = get_current_user()
    upload_file = CloudinaryUploader()

    user_id = user['id']

    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:

            title = database.query(Etech).filter_by(
                title=title_form).first()
            if title:
                return ERRO_ALREDY_EXIST('mesmo titulo em outro etech. Por favor escolha um título diferente.')

            description = database.query(Etech).filter_by(
                description=description_form).first()

            if description:
                return ERRO_ALREDY_EXIST('mesma descrição em outro etech, Por favor escolha uma descrição diferente.')

            file = request.files['file']

            url_file = upload_file.upload_file(file, public_id=title_form)

            if not url_file['success']:
                return ERRO_UPLOAD_FILE

            new_etech = Etech(user=user_id, price=price, language=language, image=url_file['secure_url'],
                              title=title_form, topics=topics, description=description_form)

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
                return ERRO_NOT_FOUND('etech')

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


def update_etech(data: EtechUpdateDTO, etech_id):
    if not data:
        return ERRO_MISS_BODY

    validation_error = update_etech_valitaions(data)
    if validation_error:
        return validation_error

    try:
        with get_database_session() as database:
            etech = database.query(Etech).filter_by(
                id=etech_id).first()

            if "title" in data:
                filtered_by_title = database.query(Etech).filter_by(
                    title=data['title']).first()
                if filtered_by_title:
                    return ERRO_ALREDY_EXIST('title')

            if "description" in data:
                filtered_by_description = database.query(Etech).filter_by(
                    description=data['description']).first()
                if filtered_by_description:
                    return ERRO_ALREDY_EXIST('description')

            for key, value in data.items():
                match key:
                    case 'title':
                        etech.title = value
                    case 'image':
                        etech.image = value
                    case 'price':
                        etech.price = value
                    case 'topics':
                        etech.topics = value
                    case 'description':
                        etech.description = value
                    case _:
                        return ERRO_BAD_REQUEST

            database.flush()
            database.refresh(etech)

            return {
                "data": {
                    **etech.to_dict()
                }
            }, 201

    except Exception as e:
        return {"error": str(e)}, 500
