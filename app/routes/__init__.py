from flask import Blueprint
from .recommendeds import recommended_bp

def init_routes(app):
    app.register_blueprint(recommended_bp, url_prefix="/users")
    """app.register_blueprint(actors_bp, url_prefix="/actors")"""