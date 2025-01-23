import os

from infra.base import Base
from dotenv import load_dotenv
from infra.database import engine

from routes import register_routes
from flask import Flask, Blueprint

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True
    PORT = 3001


api = Blueprint('api', __name__, url_prefix='/api')


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    register_routes(api)

    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    pass
    # Base.metadata.create_all(engine)
