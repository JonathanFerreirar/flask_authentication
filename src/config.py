from flask import Flask
from routes import register_routes


class Config:
    SECRET_KEY = 'mysecretkey'
    DEBUG = True
    PORT = 3001


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registra rotas
    register_routes(app)

    return app
