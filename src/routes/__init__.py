from .user_routes import user_bp
from .auth_routes import auth_bp
from .etech_routes import etech_bp
from .chapter_router import chapter_bp


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(etech_bp, url_prefix='/etechs')
    app.register_blueprint(chapter_bp, url_prefix='/chapter')
