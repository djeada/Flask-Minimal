"""
Global error handlers for the application.
"""

from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from src.exceptions import LibraryException


def register_error_handlers(app):
    """Register global error handlers."""

    @app.errorhandler(LibraryException)
    def handle_library_exception(e):
        """Handle custom library exceptions."""
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handle Marshmallow validation errors."""
        return jsonify({"error": "Validation failed", "messages": e.messages}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions."""
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(404)
    def handle_not_found(_):
        """Handle 404 errors."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_):
        """Handle 405 errors."""
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_error(_):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error"}), 500
