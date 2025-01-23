from .string import remove_space
from typing import Dict, Tuple, Union


def login_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    if not all(key in data for key in ['password', 'email']):
        return {"data": "Por favor insira um email e password."}, 400

    for key, value in data.items():
        value = remove_space(str(value))
        if not value:
            return {
                "data": f'Por favor insira um valor válido para o campo ( {key} ).'
            }, 400


def user_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    if not all(key in data for key in ['name', 'password', 'email']):
        return {"data": "Por favor insira nome, password e email."}, 400

    for key, value in data.items():
        value = remove_space(str(value))
        if not value:
            return {
                "data": f'Por favor insira um valor válido para o campo ( {key} ).'
            }, 400


def etech_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    except_by = 'image'

    if not all(key in data for key in ['user', 'price', 'title', 'topics', 'description']):
        return {"data": "Por favor insira os campos corretos."}, 400

    for key, value in data.items():
        value = remove_space(str(value))

        if key != except_by:
            if not value:
                return {
                    "data": f'Por favor insira um valor válido para o campo ( {key} ).'
                }, 400
