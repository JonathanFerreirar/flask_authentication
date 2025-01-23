from infra.base import Base
from infra.database import engine

from infra.database import config
from routes import register_routes
from flask import Flask, Blueprint


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    DEBUG = True
    PORT = 3001


api = Blueprint('api', __name__, url_prefix='/api')


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = config.get('SECRET_KEY')

    register_routes(api)

    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    Base.metadata.create_all(engine)
