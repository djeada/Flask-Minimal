"""
Database models and extensions initialization.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)
cors = CORS()


def init_extensions(app):
    """Initialize Flask extensions with app context."""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cors.init_app(app)
