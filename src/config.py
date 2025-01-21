from flask import Flask, Blueprint
from routes import register_routes


class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG = True
    PORT = 3001


api = Blueprint('api', __name__, url_prefix='/api')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(api)

    app.register_blueprint(api)

    return app
