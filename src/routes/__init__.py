from .user_routes import user_bp
from .auth_routes import auth_bp
from .etech_routes import etech_bp
from .chapter_router import chapter_bp
from .content_router import content_bp
from .comment_router import comment_bp
from .profile_router import profile_bp


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(etech_bp, url_prefix='/etechs')
    app.register_blueprint(chapter_bp, url_prefix='/chapters')
    app.register_blueprint(content_bp, url_prefix='/contents')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    app.register_blueprint(profile_bp, url_prefix='/profiles')
