from .string import remove_space
from typing import Dict, Tuple, Union


def user_validations(data: Dict[str, str]) -> Union[None, Tuple[Dict[str, str], int]]:
    if not all(key in data for key in ['name', 'password', 'email']):
        return {"data": "Por favor insira nome, password e email."}, 400

    for key, value in data.items():
        value = remove_space(str(value))
        if not value:
            return {
                "data": f'Por favor insira um valor válido para o campo ( {key} ).'
            }, 400
