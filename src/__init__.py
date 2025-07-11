"""
Application factory for Flask app creation.
"""

from typing import Optional

from flask import Flask

from src.config import get_config
from src.extensions import init_extensions


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Application factory pattern for creating Flask app instances.

    Args:
        config_name: Configuration environment name

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Add CLI commands
    register_cli_commands(app)

    return app


def register_blueprints(app: Flask) -> None:
    """Register application blueprints."""
    from src.api.auth_controllers import handle_login
    from src.api.books_crud import books_api
    from src.api.users_table_page import users_page
    from src.api.v1 import api_v1
    from src.web import web_bp

    # API v1 routes
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    # Web interface routes
    app.register_blueprint(web_bp)

    # Auth controllers (login route)
    app.register_blueprint(handle_login)

    # Books CRUD (classic /books route)
    app.register_blueprint(books_api)

    # Users table page (/users route)
    app.register_blueprint(users_page)


def register_error_handlers(app: Flask) -> None:
    """Register application error handlers."""
    from src.api.errors import register_error_handlers as register_api_errors

    register_api_errors(app)


def register_cli_commands(app: Flask) -> None:
    """Register custom CLI commands."""
    from src.cli import register_commands

    register_commands(app)
