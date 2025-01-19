from random import randrange


class User:
    def __init__(self, name, age, email):
        self.age = age
        self.name = name
        self.email = email
        self.id = randrange(0, 1000)

    def to_dict(self):
        return {
            "id": self.id,
            "age": self.age,
            "name": self.name,
            "email": self.email,
        }
