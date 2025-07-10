"""
API v1 blueprint initialization.
"""
from flask import Blueprint
from src.api.v1.auth import auth_bp
from src.api.v1.users import users_bp
from src.api.v1.books import books_bp

# Create API v1 blueprint
api_v1 = Blueprint('api_v1', __name__)

# Register sub-blueprints
api_v1.register_blueprint(auth_bp, url_prefix='/auth')
api_v1.register_blueprint(users_bp, url_prefix='/users')
api_v1.register_blueprint(books_bp, url_prefix='/books')
