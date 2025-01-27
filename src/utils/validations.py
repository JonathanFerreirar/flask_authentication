from .string import remove_space
from typing import Dict, Tuple, Union, List

from erros import ERRO_BAD_REQUEST_ETECH, ERRO_TOPIC_INVALID_ETECH, ERRO_BAD_REQUEST_CHAPTER


def validate_required_fields(data: Dict[str, str], required_fields: List[str], except_fields: List[str] = []) -> Union[None, Tuple[Dict[str, str], int]]:
    """
    Validate that all required fields are present and non-empty.
    """
    for field in required_fields:
        if field not in data and field not in except_fields:
            return {"data": f"Please enter the required field: {field}."}, 400

        if field in data and field not in except_fields:
            value = remove_space(str(data[field]))
            if not value:
                return {"data": f"Please enter a valid filed to ( {field} )."}, 400
    return None


def login_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:

    required_fields = ['email', 'password']
    return validate_required_fields(data, required_fields)


def user_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    required_fields = ['name', 'email', 'password']
    return validate_required_fields(data, required_fields)


def etech_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    except_fields = ['image']
    required_fields = ['user', 'price', 'title', 'topics', 'description']
    return validate_required_fields(data, required_fields, except_fields)


def update_etech_valitaions(data: Dict[str, str]):
    for key, value in data.items():
        match key:
            case 'title' | 'image' | 'price' | 'description':
                title = remove_space(str(value))
                if not title:
                    return {
                        "data": f'Por favor insira um valor válido para o campo ( {key} ).'
                    }, 400

            case 'topics':
                if not isinstance(value, list):
                    return ERRO_TOPIC_INVALID_ETECH

            case _:
                return ERRO_BAD_REQUEST_ETECH


def update_chapter_valitaions(data: Dict[str, str]):
    for key, value in data.items():
        match key:
            case 'title':
                title = remove_space(str(value))
                if not title:
                    return {
                        "data": f'Por favor insira um valor válido para o campo ( {key} ).'
                    }, 400
            case _:
                return ERRO_BAD_REQUEST_CHAPTER


def chapter_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:

    required_fields = ['etech', 'title', 'chapter_number']
    return validate_required_fields(data, required_fields)
