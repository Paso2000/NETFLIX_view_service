from flask import Blueprint
from .views import view_bp

def init_routes(app):
    app.register_blueprint(view_bp, url_prefix="/users")
