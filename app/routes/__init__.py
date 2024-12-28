from flask import Blueprint
from .views import view_bp
from .recommendeds import recommended_bp

def init_routes(app):
    app.register_blueprint(view_bp, url_prefix="/users", name="views_blueprint")
    app.register_blueprint(recommended_bp, url_prefix="/users", name="recommendeds_blueprint")
