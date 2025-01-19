from utils import remove_space
from models.user_model import User


users = {1: User('Jonathan Rodrigo', 17, 'jonathanferreirar@gmail.com'),
         2: User('Paloma Franciny', 19, 'palomafranciny@gmail.com'),
         3: User('Dedeia', 39, 'dedeia@gmail.com')}


def get_all_users():
    return [user.to_dict() for user in users.values()]


def create_new_user(data):
    if not all(key in data for key in ['name', 'age', 'email']):
        return {"data": "Por favor insira nome, idade e email."}, 400

    for key, value in data.items():
        value = remove_space(value)
        if not value:
            return {
                "data": f'Por favor insira um valor válido para o campo ( {key} ).'
            }, 400

    new_user = User(name=data['name'], age=data['age'], email=data['email'])
    users[len(users)+1] = new_user

    return {"data": new_user.to_dict()}, 201


def get_user_by_id(user_id):
    user = users.get(user_id)
    if not user:
        return {"data": "Usuário não encontrado."}, 404

    return {"data": user.to_dict()}, 200
