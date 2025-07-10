"""
Web interface blueprints for the Flask application.
"""

from typing import Tuple

from flask import Blueprint, Response, jsonify, render_template

from src.extensions import db

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index() -> str:
    """Home page."""
    return render_template("index.html")


@web_bp.route("/health")
def health_check() -> Tuple[Response, int]:
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        from sqlalchemy import text

        db.session.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    health_data = {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "version": "2.0.0",
    }

    status_code = 200 if health_data["status"] == "healthy" else 503
    return jsonify(health_data), status_code


@web_bp.route("/api/docs")
def api_docs() -> str:
    """API documentation page."""
    return render_template("api_docs.html")
